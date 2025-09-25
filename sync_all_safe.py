#!/usr/bin/env python3
"""
Safe full sync script with visual progress and rate limiting
"""

import asyncio
import time
from datetime import datetime, timedelta
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich import box

from wake.api import WakeAPIClient
from wake.db import SessionLocal, Product, ProductVariant, VariantStock, DistributionCenter
from wake.sync import ProductSync, SyncStateManager


console = Console()


class SafeSyncManager:
    def __init__(self):
        self.start_time = time.time()
        self.products_synced = 0
        self.errors = []
        self.rate_limit_hits = 0
        self.current_page = 1
        self.batch_size = 50
        self.dc_ids = []
        
    async def get_dc_ids(self):
        """Get distribution center IDs"""
        with SessionLocal() as db:
            dcs = db.query(DistributionCenter).all()
            self.dc_ids = [dc.id for dc in dcs]
            return len(dcs)
    
    async def get_current_status(self):
        """Get current database status"""
        with SessionLocal() as db:
            return {
                "products": db.query(Product).count(),
                "variants": db.query(ProductVariant).count(),
                "stock_records": db.query(VariantStock).count()
            }
    
    def get_resume_point_from_state(self):
        """Get resume point from sync state"""
        resume_info = SyncStateManager.get_resume_point("products")
        console.print(f"[yellow]Sync state: {resume_info['status']}[/yellow]")
        if resume_info['page'] > 1:
            console.print(f"[green]Resuming from page {resume_info['page']} (already synced {resume_info['total_synced']} products)[/green]")
        return resume_info['page']
    
    def create_status_table(self, current_status, estimated_total):
        """Create status table"""
        table = Table(title="Sync Status", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        elapsed = time.time() - self.start_time
        rate = self.products_synced / elapsed if elapsed > 0 else 0
        
        table.add_row("Products in DB", f"{current_status['products']:,}")
        table.add_row("Variants in DB", f"{current_status['variants']:,}")
        table.add_row("Stock Records", f"{current_status['stock_records']:,}")
        table.add_row("Session Synced", f"{self.products_synced:,}")
        table.add_row("Sync Rate", f"{rate:.1f} products/sec")
        table.add_row("Rate Limit Hits", str(self.rate_limit_hits))
        table.add_row("Errors", str(len(self.errors)))
        table.add_row("Estimated Total", f"~{estimated_total:,}")
        
        return table
    
    async def sync_batch(self, client, sync, products):
        """Sync a batch of products with error handling"""
        for product_data in products:
            try:
                await sync._sync_product(product_data, self.dc_ids)
                self.products_synced += 1
            except Exception as e:
                error_msg = f"SKU {product_data.get('sku', 'unknown')}: {str(e)}"
                self.errors.append(error_msg)
                if "Rate limit" in str(e):
                    self.rate_limit_hits += 1
                    # Wait extra time on rate limit
                    await asyncio.sleep(5)
    
    async def run_safe_sync(self):
        """Run the sync with safety measures"""
        # Get DC IDs
        dc_count = await self.get_dc_ids()
        console.print(f"[green]Found {dc_count} distribution centers[/green]")
        
        # Get initial status
        initial_status = await self.get_current_status()
        estimated_total = 6000  # Initial estimate
        
        async with WakeAPIClient() as client:
            sync = ProductSync(api_client=client)
            
            # Find resume point if not already set
            if self.current_page == 1:
                # Fresh sync, reset state
                SyncStateManager.start_sync("products", reset=True)
            else:
                # Resume from state
                self.current_page = self.get_resume_point_from_state()
                SyncStateManager.start_sync("products", reset=False)
            
            # Create progress bars
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeRemainingColumn(),
                console=console
            ) as progress:
                
                # Main sync task
                main_task = progress.add_task(
                    "[cyan]Syncing products...", 
                    total=estimated_total - initial_status['variants']
                )
                
                # Page task
                page_task = progress.add_task(
                    f"[yellow]Page {self.current_page}", 
                    total=self.batch_size
                )
                
                consecutive_empty = 0
                
                while consecutive_empty < 3:  # Stop after 3 empty pages
                    try:
                        # Update page description
                        progress.update(page_task, description=f"[yellow]Page {self.current_page}")
                        progress.reset(page_task)
                        
                        # Fetch page
                        products = await client.get("/produtos", params={
                            "pagina": self.current_page,
                            "quantidadeRegistros": self.batch_size
                        })
                        
                        if not products:
                            consecutive_empty += 1
                            console.print(f"[yellow]Page {self.current_page} empty ({consecutive_empty}/3)[/yellow]")
                            self.current_page += 1
                            await asyncio.sleep(1)
                            continue
                        
                        consecutive_empty = 0
                        
                        # Update estimated total if we're still finding products
                        if self.current_page * self.batch_size > estimated_total - 1000:
                            estimated_total = (self.current_page + 10) * self.batch_size
                            progress.update(main_task, total=estimated_total - initial_status['variants'])
                        
                        # Sync batch
                        for i, product_data in enumerate(products):
                            try:
                                await sync._sync_product(product_data, self.dc_ids)
                                self.products_synced += 1
                                progress.advance(main_task)
                                progress.advance(page_task)
                                
                                # Show sample every 10 products
                                if self.products_synced % 10 == 0:
                                    sku = product_data.get('sku', 'unknown')
                                    name = product_data.get('nome', '')[:50]
                                    progress.print(f"  [dim]✓ {sku}: {name}...[/dim]")
                                    
                            except Exception as e:
                                error_msg = f"SKU {product_data.get('sku', 'unknown')}: {str(e)}"
                                self.errors.append(error_msg)
                                progress.print(f"[red]  ✗ {error_msg}[/red]")
                                
                                if "Rate limit" in str(e) or "429" in str(e):
                                    self.rate_limit_hits += 1
                                    wait_time = 60  # Default wait
                                    
                                    # Try to parse retry time
                                    import re
                                    match = re.search(r"Retry after (\d+) seconds", str(e))
                                    if match:
                                        wait_time = int(match.group(1))
                                    
                                    progress.print(f"[yellow]Rate limited! Waiting {wait_time} seconds...[/yellow]")
                                    
                                    # Show countdown
                                    for remaining in range(wait_time, 0, -1):
                                        progress.update(
                                            page_task, 
                                            description=f"[red]Rate limited - {remaining}s remaining"
                                        )
                                        await asyncio.sleep(1)
                        
                        # Update sync state
                        last_sku = products[-1]["sku"] if products else None
                        SyncStateManager.update_progress(
                            "products", 
                            self.current_page, 
                            last_sku=last_sku,
                            items_synced=len(products)
                        )
                        
                        # Page complete
                        self.current_page += 1
                        
                        # Add small delay between pages
                        await asyncio.sleep(1)
                        
                    except KeyboardInterrupt:
                        progress.print("\n[yellow]Sync interrupted by user[/yellow]")
                        SyncStateManager.fail_sync("products", "Interrupted by user")
                        break
                    except Exception as e:
                        progress.print(f"[red]Unexpected error: {e}[/red]")
                        self.errors.append(str(e))
                        SyncStateManager.fail_sync("products", str(e))
                        await asyncio.sleep(5)
        
        # Final summary
        final_status = await self.get_current_status()
        self.show_final_summary(initial_status, final_status)
        
        # Mark sync as completed
        SyncStateManager.complete_sync("products", total_synced=self.products_synced)
    
    def show_final_summary(self, initial_status, final_status):
        """Show final sync summary"""
        console.print("\n" + "="*50)
        console.print("[bold green]SYNC COMPLETE[/bold green]")
        console.print("="*50 + "\n")
        
        elapsed = time.time() - self.start_time
        
        # Create summary table
        table = Table(title="Sync Summary", box=box.DOUBLE_EDGE)
        table.add_column("Metric", style="cyan")
        table.add_column("Before", style="yellow")
        table.add_column("After", style="green")
        table.add_column("Change", style="magenta")
        
        for key, label in [
            ("products", "Products"), 
            ("variants", "Variants"), 
            ("stock_records", "Stock Records")
        ]:
            before = initial_status.get(key, 0)
            after = final_status.get(key, 0)
            change = after - before
            table.add_row(
                label,
                f"{before:,}",
                f"{after:,}",
                f"+{change:,}" if change > 0 else str(change)
            )
        
        console.print(table)
        
        # Performance stats
        console.print(f"\n[cyan]Performance:[/cyan]")
        console.print(f"  • Total time: {elapsed/60:.1f} minutes")
        console.print(f"  • Products synced: {self.products_synced:,}")
        console.print(f"  • Average rate: {self.products_synced/elapsed:.1f} products/second")
        console.print(f"  • Rate limit hits: {self.rate_limit_hits}")
        
        # Errors
        if self.errors:
            console.print(f"\n[red]Errors ({len(self.errors)}):[/red]")
            for i, error in enumerate(self.errors[-10:], 1):  # Show last 10
                console.print(f"  {i}. {error}")
            if len(self.errors) > 10:
                console.print(f"  ... and {len(self.errors) - 10} more")


async def main():
    """Main entry point"""
    console.print("[bold cyan]Wake E-commerce Safe Sync[/bold cyan]\n")
    
    # Check current status
    manager = SafeSyncManager()
    current_status = await manager.get_current_status()
    
    if current_status['variants'] > 0:
        console.print(f"[yellow]Found {current_status['variants']:,} existing variants in database[/yellow]\n")
        console.print("Choose sync mode:")
        console.print("  [cyan]1[/cyan] - Resume from where it left off (faster)")
        console.print("  [cyan]2[/cyan] - Resync all products from beginning (slower)")
        console.print("  [cyan]3[/cyan] - Cancel\n")
        
        choice = console.input("[bold]Enter choice (1-3): [/bold]")
        
        if choice == "3":
            console.print("[yellow]Sync cancelled[/yellow]")
            return
        elif choice == "2":
            console.print("\n[red]⚠️  This will resync ALL products from the beginning![/red]")
            confirm = console.input("Are you sure? (yes/no): ")
            if confirm.lower() != "yes":
                console.print("[yellow]Sync cancelled[/yellow]")
                return
            manager.current_page = 1
            console.print("\n[green]Starting fresh sync from page 1...[/green]\n")
        else:
            console.print("\n[green]Resuming from last sync point...[/green]\n")
    
    try:
        await manager.run_safe_sync()
    except KeyboardInterrupt:
        console.print("\n[yellow]Sync cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Fatal error: {e}[/red]")
        raise


if __name__ == "__main__":
    asyncio.run(main())