from importlib import import_module
from pathlib import Path
import pkgutil

from app.models.base import Base

MODELS_DIR = Path(__file__).resolve().parent

for module in pkgutil.iter_modules([str(MODELS_DIR)]):
    module_name = module.name
    if module_name in {"base", "__init__"} or module_name.startswith("_"):
        continue
    import_module(f"{__name__}.{module_name}")

__all__ = ["Base"]