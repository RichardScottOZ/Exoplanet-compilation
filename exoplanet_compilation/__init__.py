"""Package interface for the Exoplanet Database Compilation project."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import re

from demo_data_generator import generate_demo_data
from exoplanet_data_sources import ExoplanetDataCollector
from exoplanet_visualizations import ExoplanetVisualizer
from main import collect_data, generate_visualizations, main, show_statistics

__all__ = [
    "ExoplanetDataCollector",
    "ExoplanetVisualizer",
    "collect_data",
    "generate_demo_data",
    "generate_visualizations",
    "main",
    "show_statistics",
]

try:
    __version__ = version("exoplanet-compilation")
except PackageNotFoundError:
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    match = re.search(r'^version = "([^"]+)"$', pyproject.read_text(), re.MULTILINE)
    __version__ = match.group(1) if match else "0.0.0"
