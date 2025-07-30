import importlib

#-------------------- Package Management --------------------

__all__ = []
__version__ = "0.1.0"
__author__ = "HysingerDev"

#-------------------- Lazy Loading Modules --------------------

_lazy_modules = [
    "config",
    "database",
    "utils",
    "logger",
    "models",
    "monitor",
    "reporter",
    "scheduler"
]

def __getattr__(name):
    if name in _lazy_modules:
        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__} has no attribute {name}")

def __dir__():
    return sorted(list(globals().keys()) + _lazy_modules)
