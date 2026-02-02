# import importlib
# import pkgutil
# import pathlib

# package_dir = pathlib.Path(__file__).parent
# __all__ = []

# # Iterate through all modules in the models package
# for module_info in pkgutil.iter_modules([str(package_dir)]):
#     module_name = module_info.name
#     if module_name == "__init__":
#         continue

#     # Import the module dynamically
#     module = importlib.import_module(f"{__name__}.{module_name}")

#     # Add module to globals so models are registered with SQLAlchemy Base
#     globals()[module_name] = module
#     __all__.append(module_name)

# Explicit imports of all models so routers can access them directly

from .customers import Customer
from .products import Product
from .suppliers import Supplier
from .invoices import Invoice, InvoiceLine
from .purchase_orders import PurchaseOrder, PurchaseOrderLine, POStatus

__all__ = [
    "Customer",
    "Product",
    "Supplier",
    "Invoice",
    "InvoiceLine",
    "PurchaseOrder",
    "PurchaseOrderLine",
    "POStatus",
]