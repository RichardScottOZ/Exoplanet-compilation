# Project Architecture

## Overview

The Exoplanet Database Compilation system is designed as a modular, extensible framework for integrating multiple exoplanet data sources, processing and enriching the data, and creating comprehensive visualizations.

## System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     Exoplanet Compilation System                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Data Sources │  │  Processing  │  │Visualization │         │
│  │   Module     │→ │    Module    │→ │   Module     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         ↓                  ↓                  ↓                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ NASA Archive │  │Unified Schema│  │ 3D Galaxy    │         │
│  │ EU Catalogue │  │Enrichment    │  │ Mass-Radius  │         │
│  │ OEC (GitHub) │  │Validation    │  │ Timeline     │         │
│  │ Demo Data    │  │Export        │  │ HZ Analysis  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Module Structure

### 1. Data Sources Module (`exoplanet_data_sources.py`)

**Purpose**: Fetch and integrate data from multiple exoplanet databases

**Key Classes**:
- `ExoplanetDataCollector`: Main data collection orchestrator

**Key Methods**:
- `fetch_nasa_exoplanet_archive()`: NASA data via astroquery
- `fetch_eu_exoplanet_catalogue()`: EU data via HTTP
- `fetch_open_exoplanet_catalogue()`: OEC data via GitHub
- `load_demo_data()`: Fallback demo data
- `create_unified_schema()`: Merge all sources
- `enrich_data()`: Calculate derived properties
- `save_data()`: Export to CSV/JSON

**Data Flow**:
```
Raw Data Sources
    ↓
Individual Fetch Methods
    ↓
Unified Schema Mapping
    ↓
Data Enrichment
    ↓
CSV/JSON Export
```

### 2. Visualization Module (`exoplanet_visualizations.py`)

**Purpose**: Create interactive and static visualizations

**Key Classes**:
- `ExoplanetVisualizer`: Main visualization generator

**Key Methods**:
- `plot_3d_galaxy_view()`: Interactive 3D spatial plot (Plotly)
- `plot_mass_radius_diagram()`: Mass vs. radius scatter (Plotly)
- `plot_discovery_timeline()`: Time series by method (Plotly)
- `plot_detection_methods()`: Pie/bar charts (Matplotlib)
- `plot_habitable_zone_analysis()`: HZ scatter plot (Plotly)
- `plot_stellar_properties()`: Multi-panel star analysis (Matplotlib)
- `create_dashboard()`: Combined interactive dashboard (Plotly)

**Visualization Types**:
```
Interactive (HTML)          Static (PNG)
- 3D Galaxy View           - Detection Methods
- Mass-Radius              - Stellar Properties
- Timeline
- HZ Analysis
- Dashboard
```

### 3. Demo Data Module (`demo_data_generator.py`)

**Purpose**: Generate realistic sample data for testing

**Key Functions**:
- `generate_demo_data(n)`: Create n sample exoplanets
- `save_demo_data()`: Export demo dataset

**Features**:
- Includes famous real exoplanets (Proxima b, TRAPPIST-1e, etc.)
- Generates realistic random planets using log-normal distributions
- Maintains physical relationships (Kepler's laws, mass-radius relation)

### 4. Command-Line Interface (`main.py`)

**Purpose**: User-friendly CLI for common operations

**Commands**:
```bash
python main.py --collect     # Data collection only
python main.py --visualize   # Visualization only
python main.py --stats       # Statistics only
python main.py --all         # Full pipeline (default)
```

### 5. Jupyter Notebook (`exoplanet_analysis.ipynb`)

**Purpose**: Interactive exploration and analysis

**Sections**:
1. Setup and imports
2. Data collection from sources
3. Unified dataset creation
4. Data enrichment
5. Exploratory analysis
6. Visualization generation
7. Custom queries and analysis
8. Results export

### 6. Testing Module (`test_system.py`)

**Purpose**: Automated testing without network dependencies

**Test Coverage**:
- Demo data generation
- Data collection and processing
- Data enrichment
- Statistics generation
- Data export (CSV/JSON)
- Visualization initialization
- End-to-end workflow

## Data Schema

### Core Fields (from sources)
```
planet_name              str      Planet designation
host_star                str      Host star name
discovery_method         str      Detection method
discovery_year           float    Year discovered
orbital_period_days      float    Orbital period
planet_radius_jupiter    float    Radius (Jupiter units)
planet_mass_jupiter      float    Mass (Jupiter units)
orbital_distance_au      float    Semi-major axis
eccentricity            float    Orbital eccentricity
equilibrium_temp_k      float    Equilibrium temperature
stellar_distance_pc     float    Distance from Earth
stellar_mass_solar      float    Star mass (solar units)
stellar_radius_solar    float    Star radius (solar units)
stellar_temp_k          float    Star temperature
ra_deg, dec_deg         float    Sky coordinates
data_source             str      Original database
```

### Derived Fields (calculated)
```
planet_radius_earth     float    Radius (Earth units)
planet_mass_earth       float    Mass (Earth units)
density_g_cm3          float    Bulk density
planet_type            str      Classification category
hz_inner_au            float    HZ inner boundary
hz_outer_au            float    HZ outer boundary
in_habitable_zone      bool     Is in HZ?
x_pc, y_pc, z_pc       float    3D galactic coordinates
```

## Technology Stack

### Core Libraries
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **astroquery**: NASA API access
- **astropy**: Astronomical calculations

### Visualization
- **plotly**: Interactive HTML visualizations
- **matplotlib**: Static publication-quality plots
- **seaborn**: Statistical visualization styling
- **bokeh**: Alternative interactive plots (optional)

### Additional
- **requests**: HTTP data fetching
- **jupyter**: Interactive notebooks
- **ipywidgets**: Interactive notebook controls

## Design Patterns

### 1. Collector Pattern
`ExoplanetDataCollector` aggregates data from multiple sources into a unified format.

### 2. Strategy Pattern
Different fetch methods for different data sources, all implementing the same interface.

### 3. Builder Pattern
`enrich_data()` progressively adds derived fields to the dataset.

### 4. Factory Pattern
Visualization methods create different types of plots from the same data.

## Extensibility Points

### Adding New Data Sources
```python
def fetch_new_source(self):
    """Add new exoplanet database."""
    # 1. Fetch data
    raw_data = requests.get('https://new-source.com/api')
    
    # 2. Parse to DataFrame
    df = pd.DataFrame(raw_data.json())
    
    # 3. Map to unified schema
    # (add to create_unified_schema method)
    
    return df
```

### Adding New Visualizations
```python
def plot_new_analysis(self):
    """Add new visualization type."""
    # Use self.data
    # Create figure
    # Save and return
    pass
```

### Adding New Derived Fields
```python
# In enrich_data() method:
self.combined_data['new_field'] = calculation(
    self.combined_data['existing_field']
)
```

## Performance Considerations

### Data Collection
- Cached results to avoid re-downloading
- Async requests possible for multiple sources
- Demo data fallback for offline use

### Processing
- Vectorized pandas operations (fast)
- Lazy evaluation where possible
- Memory-efficient for 10,000+ planets

### Visualization
- HTML files: ~5MB each (interactive)
- PNG files: ~300KB each (static)
- Dashboard combines multiple views efficiently

## Error Handling

### Network Errors
- Try-except blocks around all HTTP requests
- Automatic fallback to demo data
- Clear error messages

### Data Quality
- NaN handling for missing values
- Type validation on import
- Duplicate detection across sources

### File I/O
- Path validation before save
- JSON backup for CSV files
- Temp file cleanup in tests

## Future Enhancements

### Potential Improvements
1. **Real-time updates**: Auto-fetch new discoveries
2. **Machine learning**: Planet classification, habitability scoring
3. **Web interface**: Flask/Django web app
4. **Database backend**: PostgreSQL for large datasets
5. **API service**: RESTful API for data access
6. **More sources**: Additional specialized databases
7. **3D rendering**: Advanced VPython/PyVista visualizations
8. **Statistical analysis**: Bayesian inference, trend analysis

### Scalability
- Current: Handles 10,000+ planets easily
- With DB backend: Could scale to 100,000+
- With caching: Real-time web queries possible

## File Organization

```
Exoplanet-compilation/
├── README.md                      # Main documentation
├── USAGE.md                       # Usage examples
├── ARCHITECTURE.md                # This file
├── requirements.txt               # Dependencies
├── .gitignore                     # Git ignore rules
│
├── exoplanet_data_sources.py     # Data collection
├── exoplanet_visualizations.py   # Visualization
├── demo_data_generator.py        # Demo data
├── main.py                        # CLI interface
│
├── exoplanet_analysis.ipynb      # Jupyter notebook
├── test_system.py                # Automated tests
│
└── [Generated files]
    ├── exoplanet_combined_data.csv
    ├── exoplanet_combined_data.json
    ├── exoplanet_3d_view.html
    ├── exoplanet_mass_radius.html
    ├── exoplanet_discovery_timeline.html
    ├── exoplanet_habitable_zone.html
    ├── exoplanet_dashboard.html
    ├── detection_methods.png
    └── stellar_properties.png
```

## Dependencies Graph

```
main.py
  └─→ exoplanet_data_sources.py
        └─→ demo_data_generator.py
        └─→ pandas, numpy, astroquery
  └─→ exoplanet_visualizations.py
        └─→ pandas, plotly, matplotlib

exoplanet_analysis.ipynb
  └─→ exoplanet_data_sources.py
  └─→ exoplanet_visualizations.py

test_system.py
  └─→ demo_data_generator.py
  └─→ exoplanet_data_sources.py
  └─→ exoplanet_visualizations.py
```

## API Reference

See individual module docstrings for detailed API documentation:
- `help(ExoplanetDataCollector)`
- `help(ExoplanetVisualizer)`
- `help(generate_demo_data)`

---

*Last updated: 2024*
*Version: 1.0.0*
