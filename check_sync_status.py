#!/usr/bin/env python3
"""
Check sync status for all sync types
"""

from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box

from wake.sync import SyncStateManager
from wake.db import SessionLocal, Product, ProductVariant, DistributionCenter, Category


console = Console()


def format_datetime(dt):
    """Format datetime for display"""
    if not dt:
        return "-"
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_duration(start, end):
    """Calculate and format duration"""
    if not start:
        return "-"
    if not end:
        end = datetime.now()
    
    duration = end - start
    hours = int(duration.total_seconds() // 3600)
    minutes = int((duration.total_seconds() % 3600) // 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def main():
    """Display sync status"""
    console.print("[bold cyan]Wake Sync Status[/bold cyan]\n")
    
    # Get all sync states
    states = SyncStateManager.get_all_states()
    
    # Get database counts
    with SessionLocal() as db:
        counts = {
            "distribution_centers": db.query(DistributionCenter).count(),
            "categories": db.query(Category).count(),
            "products": db.query(Product).count(),
            "variants": db.query(ProductVariant).count()
        }
    
    # Create status table
    table = Table(title="Sync Status", box=box.ROUNDED)
    table.add_column("Sync Type", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Last Page", style="yellow")
    table.add_column("Total Synced", style="magenta")
    table.add_column("Started At", style="blue")
    table.add_column("Duration", style="white")
    table.add_column("Error", style="red")
    
    # Define sync types to show
    sync_types = [
        ("products", "Products (Full)"),
        ("products_only", "Products (No Price/Stock)"),
        ("prices", "Prices"),
        ("stock", "Stock"),
        ("categories", "Categories"),
        ("distribution_centers", "Distribution Centers")
    ]
    
    # Add status for each sync type
    for sync_key, display_name in sync_types:
        if sync_key in states:
            state = states[sync_key]
            status_style = {
                "running": "[yellow]Running[/yellow]",
                "completed": "[green]Completed[/green]",
                "failed": "[red]Failed[/red]",
                "idle": "[dim]Idle[/dim]"
            }.get(state["status"], state["status"])
            
            table.add_row(
                display_name,
                status_style,
                str(state["last_page"]) if state["last_page"] else "-",
                f"{state['total_synced']:,}" if state['total_synced'] else "-",
                format_datetime(state["started_at"]),
                format_duration(state["started_at"], state["completed_at"]),
                (state["error_message"][:30] + "...") if state["error_message"] and len(state["error_message"]) > 30 else state["error_message"] or "-"
            )
        else:
            table.add_row(display_name, "[dim]Never run[/dim]", "-", "-", "-", "-", "-")
    
    console.print(table)
    
    # Database summary
    console.print("\n[bold]Database Summary:[/bold]")
    console.print(f"  • Distribution Centers: {counts['distribution_centers']:,}")
    console.print(f"  • Categories: {counts['categories']:,}")
    console.print(f"  • Products: {counts['products']:,}")
    console.print(f"  • Product Variants: {counts['variants']:,}")
    
    # Resume instructions
    if "products" in states and states["products"]["status"] in ["running", "failed"]:
        console.print("\n[yellow]Note: Products sync can be resumed by running sync_all_safe.py[/yellow]")


if __name__ == "__main__":
    main()