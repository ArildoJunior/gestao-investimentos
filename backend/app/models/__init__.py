from importlib import import_module
from pathlib import Path

from app.models.base import Base

_models_dir = Path(__file__).parent

for file in _models_dir.glob("*.py"):
    module_name = file.stem
    if module_name in {"__init__", "base"} or module_name.startswith("_"):
        continue
    import_module(f"{__name__}.{module_name}")

__all__ = ["Base"]