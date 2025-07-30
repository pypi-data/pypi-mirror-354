#register your own engine into 'fastbackfilter/engines/' and it will auto-register here.
from importlib import import_module
from pathlib import Path
_pkg_dir = Path(__file__).resolve().parent
for _file in _pkg_dir.glob("*.py"):
    if _file.stem != "__init__":
        import_module(f"{__name__}.{_file.stem}")
