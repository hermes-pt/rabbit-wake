#!/usr/bin/env python3
"""
Sync only stock data for existing products
This is the most frequent sync - run multiple times per day
"""

import asyncio
import time
from datetime import datetime, timedelta
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich import box

from wake.api import WakeAPIClient
from wake.sync import StockSync, SyncStateManager
from wake.db import SessionLocal, VariantStock, ProductVariant


console = Console()


async def sync_stock():
    """Sync stock levels for all products"""
    console.print("[bold cyan]Wake Stock Sync[/bold cyan]")
    console.print("[yellow]This will update stock levels for existing products[/yellow]\n")
    
    # Get current stock stats
    with SessionLocal() as db:
        total_variants = db.query(ProductVariant).count()
        # Count distinct variants with stock > 0
        from sqlalchemy import func
        variants_with_stock = db.query(func.count(func.distinct(VariantStock.variant_id))).filter(VariantStock.physical_stock > 0).scalar() or 0
    
    console.print(f"Current: {total_variants:,} variants, {variants_with_stock:,} with stock > 0\n")
    
    # Check for recent changes
    console.print("Sync mode:")
    console.print("  1. All stock levels (recommended)")
    console.print("  2. Only recent changes (last 48 hours)")
    choice = console.input("\nChoice (1-2): ")
    
    # Start sync state
    SyncStateManager.start_sync("stock", reset=True)
    
    start_time = time.time()
    total_updated = 0
    
    async with WakeAPIClient() as client:
        sync = StockSync(api_client=client)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            
            if choice == "2":
                # Sync only recent changes
                since_date = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d")
                task = progress.add_task("[cyan]Syncing stock changes...", total=None)
                
                try:
                    total_updated = await sync.sync_stock_changes(changed_since=since_date)
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
                    SyncStateManager.fail_sync("stock", str(e))
                    return
            else:
                # Sync all stock
                task = progress.add_task("[cyan]Syncing all stock levels...", total=total_variants * 3)  # 3 DCs
                
                try:
                    # Process in batches with progress
                    batch_size = 50
                    processed = 0
                    
                    with SessionLocal() as db:
                        offset = 0
                        
                        while True:
                            variants = db.query(ProductVariant).offset(offset).limit(batch_size).all()
                            
                            if not variants:
                                break
                            
                            for variant in variants:
                                updated = await sync._sync_variant_stock(variant.id, variant.sku)
                                total_updated += updated
                                processed += 3  # 3 DCs per variant
                                progress.update(task, completed=processed)
                            
                            offset += batch_size
                            
                            # Update sync state periodically
                            if offset % 200 == 0:
                                SyncStateManager.update_progress(
                                    "stock",
                                    offset // batch_size,
                                    items_synced=total_updated
                                )
                            
                            await asyncio.sleep(0.1)  # Rate limit protection
                    
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
                    SyncStateManager.fail_sync("stock", str(e))
                    return
    
    # Complete
    SyncStateManager.complete_sync("stock", total_synced=total_updated)
    
    elapsed = time.time() - start_time
    console.print(f"\n[green]✓ Updated {total_updated:,} stock records in {elapsed/60:.1f} minutes[/green]")
    
    # Show stock summary
    with SessionLocal() as db:
        new_variants_with_stock = db.query(func.count(func.distinct(VariantStock.variant_id))).filter(VariantStock.physical_stock > 0).scalar() or 0
        total_units = db.query(func.sum(VariantStock.physical_stock)).scalar() or 0
    
    # Create summary table
    table = Table(title="Stock Summary", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Variants with stock > 0", f"{new_variants_with_stock:,}")
    table.add_row("Change", f"{new_variants_with_stock - variants_with_stock:+,}")
    table.add_row("Total units in stock", f"{total_units:,}")
    table.add_row("Sync rate", f"{total_updated/elapsed:.1f} records/second")
    
    console.print("\n", table)


if __name__ == "__main__":
    asyncio.run(sync_stock())