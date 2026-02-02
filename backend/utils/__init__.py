import importlib
import pkgutil
import pathlib

package_dir = pathlib.Path(__file__).parent
__all__ = []

# Iterate through all modules in the utils package
for module_info in pkgutil.iter_modules([str(package_dir)]):
    module_name = module_info.name
    if module_name == "__init__":
        continue

    # Import the module dynamically
    module = importlib.import_module(f"{__name__}.{module_name}")

    # Add module to __all__ for clean imports
    globals()[module_name] = module
    __all__.append(module_name)
