#!/usr/bin/env python3
"""
Sync only product data (without prices and stock)
Much faster than full sync - use for adding new products
"""

import asyncio
import time
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn

from wake.api import WakeAPIClient
from wake.sync import ProductSync, SyncStateManager
from wake.db import SessionLocal, Product, ProductVariant


console = Console()


async def sync_products_only():
    """Sync only product data"""
    console.print("[bold cyan]Wake Products-Only Sync[/bold cyan]")
    console.print("[yellow]This will sync product data WITHOUT prices and stock[/yellow]\n")
    
    # Check current status
    with SessionLocal() as db:
        current_products = db.query(Product).count()
        current_variants = db.query(ProductVariant).count()
    
    console.print(f"Current database: {current_products:,} products, {current_variants:,} variants\n")
    
    # Get sync state
    resume_info = SyncStateManager.get_resume_point("products_only")
    
    if resume_info['page'] > 1:
        console.print(f"[yellow]Found incomplete sync at page {resume_info['page']}[/yellow]")
        console.print("Resume from last position? (y/n): ", end="")
        if input().lower() != 'y':
            resume_info['page'] = 1
            SyncStateManager.start_sync("products_only", reset=True)
        else:
            SyncStateManager.start_sync("products_only", reset=False)
    else:
        SyncStateManager.start_sync("products_only", reset=True)
    
    start_time = time.time()
    total_synced = 0
    current_page = resume_info['page']
    
    async with WakeAPIClient() as client:
        # Create sync without price and stock sync
        sync = ProductSync(api_client=client, sync_prices=False, sync_stock=False)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task("[cyan]Syncing products...", total=None)
            
            consecutive_empty = 0
            
            while consecutive_empty < 3:
                try:
                    # Get page
                    products = await client.get("/produtos", params={
                        "pagina": current_page,
                        "quantidadeRegistros": 50,
                        "camposAdicionais": ["Atributo", "Informacao"]
                    })
                    
                    if not products:
                        consecutive_empty += 1
                        current_page += 1
                        continue
                    
                    consecutive_empty = 0
                    
                    # Sync products
                    for product_data in products:
                        await sync._sync_product(product_data, [])  # Empty DC list since no stock
                        total_synced += 1
                        
                        if total_synced % 10 == 0:
                            progress.update(task, description=f"[cyan]Syncing products... {total_synced:,} done")
                    
                    # Update state
                    SyncStateManager.update_progress(
                        "products_only",
                        current_page,
                        last_sku=products[-1]["sku"] if products else None,
                        items_synced=len(products)
                    )
                    
                    current_page += 1
                    await asyncio.sleep(0.5)  # Rate limit protection
                    
                except KeyboardInterrupt:
                    console.print("\n[yellow]Sync interrupted[/yellow]")
                    SyncStateManager.fail_sync("products_only", "Interrupted by user")
                    break
                except Exception as e:
                    console.print(f"\n[red]Error: {e}[/red]")
                    SyncStateManager.fail_sync("products_only", str(e))
                    break
    
    # Complete
    SyncStateManager.complete_sync("products_only", total_synced=total_synced)
    
    elapsed = time.time() - start_time
    console.print(f"\n[green]✓ Synced {total_synced:,} products in {elapsed/60:.1f} minutes[/green]")
    console.print(f"[cyan]Rate: {total_synced/elapsed:.1f} products/second[/cyan]")
    
    # Show new counts
    with SessionLocal() as db:
        new_products = db.query(Product).count()
        new_variants = db.query(ProductVariant).count()
    
    console.print(f"\nDatabase now has: {new_products:,} products, {new_variants:,} variants")
    console.print(f"Added: {new_products - current_products:,} products, {new_variants - current_variants:,} variants")


if __name__ == "__main__":
    asyncio.run(sync_products_only())