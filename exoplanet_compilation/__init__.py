"""Package interface for the Exoplanet Database Compilation project."""

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

__version__ = "0.1.0"
