"""cds_helper init."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cdshelper")
except PackageNotFoundError:
    # package is not installed
    print("package is not installed")
    pass
