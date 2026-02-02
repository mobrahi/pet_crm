import importlib
import pkgutil
import pathlib

# Path to this package (backend/routers)
package_dir = pathlib.Path(__file__).parent

all_routers = []

# Iterate through all modules in the routers package
for module_info in pkgutil.iter_modules([str(package_dir)]):
    module_name = module_info.name
    # Skip __init__.py itself
    if module_name == "__init__":
        continue

    # Import the module dynamically
    module = importlib.import_module(f"{__name__}.{module_name}")

    # If the module has a "router" attribute, add it
    if hasattr(module, "router"):
        all_routers.append(module.router)
