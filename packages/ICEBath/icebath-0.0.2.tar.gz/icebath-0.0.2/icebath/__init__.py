from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("icebath")
except PackageNotFoundError:
    # package is not installed
    pass
