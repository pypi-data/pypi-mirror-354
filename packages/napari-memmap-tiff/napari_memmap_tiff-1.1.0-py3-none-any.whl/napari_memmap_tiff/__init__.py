try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
from ._widget import memmap_config_widget

__all__ = ("memmap_config_widget",)
