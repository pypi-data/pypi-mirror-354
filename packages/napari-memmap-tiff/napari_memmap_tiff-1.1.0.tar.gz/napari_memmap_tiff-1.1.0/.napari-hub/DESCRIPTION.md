When installed and enabled in the options, it adds an option that when enabled
will make napari load tiffs via memory mapping instead of fully into RAM.

That is, `.tif` and `.tiff` files will be loaded into memory using memory
mapping, which loads the data directly from disk instead of loading the file
at once into RAM. This is beneficial for large files that may not fit into
available RAM.
