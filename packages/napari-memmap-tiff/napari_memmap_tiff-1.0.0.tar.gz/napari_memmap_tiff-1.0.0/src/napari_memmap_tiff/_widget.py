from typing import TYPE_CHECKING

import numpy as np
from imageio.config.extensions import extension_list
from imageio.config.plugins import PluginConfig, known_plugins
from imageio.plugins.tifffile_v3 import TifffilePlugin
from magicgui import magic_factory

if TYPE_CHECKING:
    pass


class MemmapTifffilePlugin(TifffilePlugin):

    def read(self, *args, **kwargs) -> np.ndarray:
        return super().read(*args, **kwargs, out="memmap")


@magic_factory(auto_call=True, persist=False)
def memmap_config_widget(
    enable_memory_map: bool,
) -> None:
    """
    Sets whether to use memory mapping.

    :param enable_memory_map: If enabled, tiff or tif files will be loaded as
        memory mapped data directly from disk, instead of loading it fully into
        memory at once.
    """
    if enable_memory_map:
        if "tifffile_memmap" in known_plugins:
            return

        known_plugins["tifffile_memmap"] = PluginConfig(
            name="tifffile_memmap",
            class_name="MemmapTifffilePlugin",
            module_name="napari_memmap_tiff._widget",
            is_legacy=False,
        )
        for ext in extension_list:
            if (
                ext.extension in (".tif", ".tiff")
                and "tifffile_memmap" not in ext.priority
            ):
                ext.priority.insert(0, "tifffile_memmap")
    else:
        if "tifffile_memmap" not in known_plugins:
            return

        del known_plugins["tifffile_memmap"]
        for ext in extension_list:
            if (
                ext.extension in (".tif", ".tiff")
                and "tifffile_memmap" in ext.priority
            ):
                ext.priority.remove("tifffile_memmap")
