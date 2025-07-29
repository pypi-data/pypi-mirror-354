"""OpenCar - Advanced Autonomous Vehicle Perception System."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("opencar")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["__version__"] 