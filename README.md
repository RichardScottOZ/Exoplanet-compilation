# Exoplanet Database Compilation & Visualization

A comprehensive system for integrating, analyzing, and visualizing data from multiple exoplanet databases into one cohesive whole.

## 🌟 Features

- **Multi-Source Integration**: Automatically fetches and merges data from major exoplanet databases
- **Unified Data Schema**: Harmonizes different data formats into a single, consistent structure
- **Rich Visualizations**: Interactive 3D views, charts, and dashboards
- **Data Enrichment**: Calculates derived properties like habitable zone status, planet types, and more
- **Easy to Use**: Simple Python API and Jupyter notebook interface

## 📊 Integrated Databases

This project integrates data from the following authoritative sources:

1. **NASA Exoplanet Archive** ([exoplanetarchive.ipac.caltech.edu](https://exoplanetarchive.ipac.caltech.edu/))
   - Comprehensive database maintained by NASA/IPAC
   - Planetary Systems Composite Parameters table
   - Most complete and well-maintained source

2. **EU Exoplanet Catalogue** ([exoplanet.eu](http://exoplanet.eu/))
   - European-based exoplanet database
   - Maintained by Paris Observatory
   - Alternative measurements and parameters

3. **Open Exoplanet Catalogue** ([openexoplanetcatalogue.com](http://www.openexoplanetcatalogue.com/))
   - Community-maintained open-source database
   - GitHub-based collaborative effort
   - XML-based comprehensive catalog

4. **Exoplanet Orbit Database** ([exoplanets.org](http://exoplanets.org/))
   - Specialized in orbital parameters
   - Detailed orbital mechanics data

5. **TEPCat** (Transiting Extrasolar Planet Catalogue)
   - Specialized database for transiting exoplanets
   - High-precision transit parameters

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/RichardScottOZ/Exoplanet-compilation.git
cd Exoplanet-compilation

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

#### 1. Collect and Integrate Data

```python
from exoplanet_data_sources import ExoplanetDataCollector

# Initialize collector
collector = ExoplanetDataCollector()

# Fetch from all sources
collector.fetch_nasa_exoplanet_archive()
collector.fetch_eu_exoplanet_catalogue()

# Create unified dataset
combined_data = collector.create_unified_schema()

# Enrich with derived values
enriched_data = collector.enrich_data()

# Show statistics
collector.get_statistics()

# Save to file
collector.save_data('exoplanet_combined_data.csv')
```

#### 2. Create Visualizations

```python
from exoplanet_visualizations import ExoplanetVisualizer
import pandas as pd

# Load data
data = pd.read_csv('exoplanet_combined_data.csv')

# Create visualizer
viz = ExoplanetVisualizer(data)

# Generate all visualizations
viz.generate_all_visualizations()
```

#### 3. Interactive Analysis (Jupyter Notebook)

```bash
# Launch Jupyter
jupyter notebook exoplanet_analysis.ipynb
```

## 📈 Visualizations

The system generates multiple types of visualizations:

### 1. 3D Galaxy View
Interactive 3D scatter plot showing the spatial distribution of exoplanets around our solar system.
- **File**: `exoplanet_3d_view.html`
- **Features**: Zoomable, rotatable, color-coded by planet type or detection method

### 2. Mass-Radius Diagram
Log-scale scatter plot comparing exoplanet masses and radii.
- **File**: `exoplanet_mass_radius.html`
- **Features**: Planet type classification, reference lines for Earth and Jupiter

### 3. Discovery Timeline
Area chart showing exoplanet discoveries over time by detection method.
- **File**: `exoplanet_discovery_timeline.html`
- **Features**: Stacked by detection method, interactive timeline

### 4. Detection Methods Analysis
Pie chart and bar chart breakdown of detection methods.
- **File**: `detection_methods.png`
- **Features**: Shows distribution of Transit, Radial Velocity, Direct Imaging, etc.

### 5. Habitable Zone Analysis
Scatter plot of orbital distance vs. temperature, highlighting potentially habitable planets.
- **File**: `exoplanet_habitable_zone.html`
- **Features**: Green highlighting for habitable zone, sized by planet radius

### 6. Stellar Properties
Multi-panel analysis of host star characteristics.
- **File**: `stellar_properties.png`
- **Features**: Mass distribution, temperature distribution, HR diagram, distance distribution

### 7. Comprehensive Dashboard
All-in-one interactive dashboard with multiple views.
- **File**: `exoplanet_dashboard.html`
- **Features**: Detection methods, planet types, timeline, mass-radius in one view

## 📋 Data Schema

The unified dataset includes the following fields:

### Planet Properties
- `planet_name`: Official planet designation
- `planet_radius_jupiter`: Radius in Jupiter radii
- `planet_radius_earth`: Radius in Earth radii (derived)
- `planet_mass_jupiter`: Mass in Jupiter masses
- `planet_mass_earth`: Mass in Earth masses (derived)
- `planet_type`: Classification (Rocky, Super-Earth, Neptune-like, Jupiter-like)
- `density_g_cm3`: Bulk density (derived)

### Orbital Properties
- `orbital_period_days`: Orbital period
- `orbital_distance_au`: Semi-major axis in AU
- `eccentricity`: Orbital eccentricity
- `equilibrium_temp_k`: Equilibrium temperature

### Host Star Properties
- `host_star`: Name of host star
- `stellar_mass_solar`: Mass in solar masses
- `stellar_radius_solar`: Radius in solar radii
- `stellar_temp_k`: Effective temperature
- `stellar_distance_pc`: Distance from Earth in parsecs

### Position & Discovery
- `ra_deg`, `dec_deg`: Sky coordinates
- `x_pc`, `y_pc`, `z_pc`: 3D galactic coordinates (derived)
- `discovery_method`: Detection method used
- `discovery_year`: Year of discovery
- `data_source`: Original database source

### Habitability
- `hz_inner_au`, `hz_outer_au`: Habitable zone boundaries (derived)
- `in_habitable_zone`: Boolean flag (derived)

## 🔬 Advanced Features

### Habitable Planet Search

```python
# Find potentially habitable Earth-like planets
habitable = data[
    (data['in_habitable_zone'] == True) &
    (data['planet_type'] == 'Rocky (Earth-like)')
].sort_values('stellar_distance_pc')

print(habitable[['planet_name', 'stellar_distance_pc', 'equilibrium_temp_k']])
```

### Custom Analysis

```python
# Statistical analysis by detection method
method_stats = data.groupby('discovery_method').agg({
    'planet_name': 'count',
    'planet_mass_earth': 'mean',
    'stellar_distance_pc': 'mean'
})
```

### Data Export

All visualizations are saved as:
- **Interactive HTML** files (Plotly) - Open in any web browser
- **High-resolution PNG** files (Matplotlib) - For publications
- **CSV/JSON** data files - For further analysis

## 🛠️ Technical Details

### Dependencies
- `pandas`, `numpy` - Data manipulation
- `astroquery` - NASA Exoplanet Archive API
- `astropy` - Astronomical calculations
- `matplotlib`, `seaborn` - Static visualizations
- `plotly`, `bokeh` - Interactive visualizations
- `jupyter` - Notebook interface

### Data Quality
- Automatic duplicate removal across sources
- Missing data handling with NaN values
- Data validation and type checking
- Source attribution for each record

### Performance
- Efficient pandas operations
- Parallel-safe visualization generation
- Cached data loading
- Memory-optimized for large datasets (10,000+ planets)

## 📝 Examples

### Example 1: Quick Data Fetch
```bash
python exoplanet_data_sources.py
```

### Example 2: Generate All Visualizations
```bash
python exoplanet_visualizations.py
```

### Example 3: Interactive Notebook
```bash
jupyter notebook exoplanet_analysis.ipynb
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional database integrations
- New visualization types
- Performance optimizations
- Documentation improvements
- Bug fixes

## 📄 License

This project is open source and available for scientific and educational use.

## 🙏 Acknowledgments

Data sources:
- NASA Exoplanet Science Institute
- Paris Observatory (exoplanet.eu)
- Open Exoplanet Catalogue community
- Exoplanet Orbit Database team
- TEPCat maintainers

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

## 🌌 Fun Facts

As of 2024, over 5,500 confirmed exoplanets have been discovered!
- First confirmed: 1992 (around pulsar PSR B1257+12)
- Most common detection method: Transit photometry (thanks to Kepler & TESS)
- Closest: Proxima Centauri b (~4.2 light-years)
- Largest known: ROXs 42Bb (2.5x Jupiter's radius)
- Potentially habitable: Dozens in the habitable zone of their stars!
