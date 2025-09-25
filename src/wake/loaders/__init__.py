"""Wake data loaders"""

from .products import ProductsLoader
from .stock_locations import StockLocationsLoader
from .categories import CategoriesLoader

__all__ = ["ProductsLoader", "StockLocationsLoader", "CategoriesLoader"]