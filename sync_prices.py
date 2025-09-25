#!/usr/bin/env python3
"""
Sync only price data for existing products
Fast sync for keeping prices up to date
"""

import asyncio
import time
from datetime import datetime, timedelta
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from wake.api import WakeAPIClient
from wake.sync import PriceSync, SyncStateManager
from wake.db import SessionLocal, VariantPricing


console = Console()


async def sync_prices():
    """Sync prices for all products"""
    console.print("[bold cyan]Wake Price Sync[/bold cyan]")
    console.print("[yellow]This will update prices for existing products only[/yellow]\n")
    
    # Check for recent changes
    console.print("Sync mode:")
    console.print("  1. All prices (slower, more thorough)")
    console.print("  2. Only recent changes (last 48 hours)")
    choice = console.input("\nChoice (1-2): ")
    
    # Start sync state
    SyncStateManager.start_sync("prices", reset=True)
    
    start_time = time.time()
    total_updated = 0
    
    async with WakeAPIClient() as client:
        sync = PriceSync(api_client=client)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            
            if choice == "2":
                # Sync only recent changes
                since_date = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d")
                task = progress.add_task("[cyan]Syncing price changes...", total=None)
                
                try:
                    total_updated = await sync.sync_price_changes(changed_since=since_date)
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
                    SyncStateManager.fail_sync("prices", str(e))
                    return
            else:
                # Sync all prices
                task = progress.add_task("[cyan]Syncing all prices...", total=None)
                
                try:
                    # Get current price count
                    with SessionLocal() as db:
                        current_prices = db.query(VariantPricing).count()
                    
                    total_updated = await sync.sync_all_prices()
                    
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
                    SyncStateManager.fail_sync("prices", str(e))
                    return
    
    # Complete
    SyncStateManager.complete_sync("prices", total_synced=total_updated)
    
    elapsed = time.time() - start_time
    console.print(f"\n[green]✓ Updated {total_updated:,} prices in {elapsed:.1f} seconds[/green]")
    
    # Show some price examples
    with SessionLocal() as db:
        sample_prices = db.query(VariantPricing).limit(5).all()
        if sample_prices:
            console.print("\n[cyan]Sample prices:[/cyan]")
            for price in sample_prices:
                if price.original_price and price.sale_price:
                    discount = ((price.original_price - price.sale_price) / price.original_price) * 100
                    console.print(f"  Variant {price.variant_id}: R$ {price.original_price:.2f} → R$ {price.sale_price:.2f} ({discount:.0f}% off)")


if __name__ == "__main__":
    asyncio.run(sync_prices())