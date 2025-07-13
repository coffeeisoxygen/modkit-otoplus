import importlib
import pkgutil
from pathlib import Path

# Path ke folder ini (yaitu backend/models/)
package_dir = Path(__file__).resolve().parent

# Loop semua file di dalam folder ini, kecuali __init__.py
for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
    if not module_name.startswith("__"):
        # Import backend.models.<module_name>
        importlib.import_module(f"{__name__}.{module_name}")
