# Usage Examples and Tutorials

This document provides detailed examples of how to use the Exoplanet Database Compilation system.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Data Collection](#data-collection)
3. [Data Analysis](#data-analysis)
4. [Visualizations](#visualizations)
5. [Custom Queries](#custom-queries)
6. [Advanced Usage](#advanced-usage)

---

## Quick Start

### Option 1: Command Line (Easiest)

```bash
# Run the complete pipeline (collect data + create visualizations)
python main.py

# Or run specific steps
python main.py --collect        # Only collect data
python main.py --visualize      # Only create visualizations
python main.py --stats          # Only show statistics
```

### Option 2: Python Script

```python
from exoplanet_data_sources import ExoplanetDataCollector
from exoplanet_visualizations import ExoplanetVisualizer

# Collect data
collector = ExoplanetDataCollector()
collector.fetch_nasa_exoplanet_archive()
collector.fetch_eu_exoplanet_catalogue()
data = collector.create_unified_schema()
enriched_data = collector.enrich_data()
collector.save_data('my_exoplanet_data.csv')

# Create visualizations
viz = ExoplanetVisualizer(enriched_data)
viz.generate_all_visualizations()
```

### Option 3: Jupyter Notebook (Most Interactive)

```bash
jupyter notebook exoplanet_analysis.ipynb
```

---

## Data Collection

### Fetching from Individual Sources

```python
from exoplanet_data_sources import ExoplanetDataCollector

collector = ExoplanetDataCollector()

# NASA Exoplanet Archive (most comprehensive)
nasa_data = collector.fetch_nasa_exoplanet_archive()
print(f"NASA: {len(nasa_data)} planets")

# EU Exoplanet Catalogue
eu_data = collector.fetch_eu_exoplanet_catalogue()
print(f"EU: {len(eu_data)} planets")

# Open Exoplanet Catalogue (optional)
# oec_data = collector.fetch_open_exoplanet_catalogue()
```

### Creating Unified Dataset

```python
# Merge all sources into unified schema
combined_data = collector.create_unified_schema()
print(f"Total unique planets: {len(combined_data)}")

# Add derived properties
enriched_data = collector.enrich_data()

# Available derived columns:
# - planet_radius_earth, planet_mass_earth
# - density_g_cm3
# - planet_type (classification)
# - hz_inner_au, hz_outer_au (habitable zone)
# - in_habitable_zone (boolean)
# - x_pc, y_pc, z_pc (3D coordinates)
```

### Saving Data

```python
# Save as CSV
collector.save_data('exoplanet_data.csv')

# Data is automatically saved as both CSV and JSON
# - exoplanet_data.csv (tabular format)
# - exoplanet_data.json (hierarchical format)
```

### Using Demo Data (Offline Mode)

```python
# If network is unavailable, use demo data
collector.load_demo_data()
data = collector.create_unified_schema()
enriched_data = collector.enrich_data()
```

---

## Data Analysis

### Loading Saved Data

```python
import pandas as pd

# Load previously saved data
data = pd.read_csv('exoplanet_combined_data.csv')
print(data.shape)
print(data.columns)
```

### Basic Statistics

```python
# Get summary statistics
collector.get_statistics()

# Or manually analyze
print(f"Total planets: {len(data)}")
print(f"Discovery methods: {data['discovery_method'].nunique()}")
print(f"Year range: {data['discovery_year'].min()}-{data['discovery_year'].max()}")
```

### Filtering Data

```python
# Find Earth-like planets
earth_like = data[data['planet_type'] == 'Rocky (Earth-like)']
print(f"Earth-like planets: {len(earth_like)}")

# Find planets in habitable zone
habitable = data[data['in_habitable_zone'] == True]
print(f"Habitable zone planets: {len(habitable)}")

# Find nearby systems (within 100 parsecs)
nearby = data[data['stellar_distance_pc'] < 100]
print(f"Nearby systems: {len(nearby)}")

# Combine filters
potentially_habitable = data[
    (data['in_habitable_zone'] == True) &
    (data['planet_type'].isin(['Rocky (Earth-like)', 'Super-Earth'])) &
    (data['stellar_distance_pc'] < 100)
].sort_values('stellar_distance_pc')

print("\nClosest potentially habitable planets:")
print(potentially_habitable[['planet_name', 'stellar_distance_pc', 'equilibrium_temp_k']].head())
```

### Grouping and Aggregation

```python
# Statistics by detection method
method_stats = data.groupby('discovery_method').agg({
    'planet_name': 'count',
    'planet_mass_earth': 'mean',
    'planet_radius_earth': 'mean',
    'stellar_distance_pc': 'mean'
}).round(2)
method_stats.columns = ['Count', 'Avg Mass', 'Avg Radius', 'Avg Distance']
print(method_stats)

# Discoveries per year
yearly = data.groupby('discovery_year')['planet_name'].count()
print(f"\nMost productive year: {yearly.idxmax()} with {yearly.max()} discoveries")

# Planets per host star
multi_planet = data.groupby('host_star').size().sort_values(ascending=False)
print(f"\nSystems with most planets:")
print(multi_planet.head())
```

---

## Visualizations

### Creating Individual Visualizations

```python
from exoplanet_visualizations import ExoplanetVisualizer
import pandas as pd

data = pd.read_csv('exoplanet_combined_data.csv')
viz = ExoplanetVisualizer(data)

# 3D spatial distribution
fig_3d = viz.plot_3d_galaxy_view(save_html=True)
# Opens as: exoplanet_3d_view.html

# Mass-Radius diagram
fig_mr = viz.plot_mass_radius_diagram(save_html=True)
# Opens as: exoplanet_mass_radius.html

# Discovery timeline
fig_timeline = viz.plot_discovery_timeline(save_html=True)
# Opens as: exoplanet_discovery_timeline.html

# Detection methods analysis
fig_methods = viz.plot_detection_methods()
# Saves as: detection_methods.png

# Habitable zone analysis
fig_hz = viz.plot_habitable_zone_analysis(save_html=True)
# Opens as: exoplanet_habitable_zone.html

# Stellar properties
fig_stellar = viz.plot_stellar_properties()
# Saves as: stellar_properties.png

# Comprehensive dashboard
fig_dashboard = viz.create_dashboard(save_html=True)
# Opens as: exoplanet_dashboard.html
```

### Generate All at Once

```python
# Create all visualizations with one command
viz.generate_all_visualizations()
```

### Opening Interactive Visualizations

```bash
# HTML files can be opened in any web browser
firefox exoplanet_3d_view.html
chrome exoplanet_dashboard.html
open exoplanet_mass_radius.html  # macOS
```

---

## Custom Queries

### Find Specific Types of Planets

```python
# Hot Jupiters (close-in gas giants)
hot_jupiters = data[
    (data['planet_type'] == 'Jupiter-like') &
    (data['orbital_distance_au'] < 0.1)
]
print(f"Hot Jupiters: {len(hot_jupiters)}")

# Super-Earths in habitable zone
super_earth_hz = data[
    (data['planet_type'] == 'Super-Earth') &
    (data['in_habitable_zone'] == True)
]
print(f"Habitable zone Super-Earths: {len(super_earth_hz)}")

# Planets around M-dwarfs
m_dwarf_planets = data[data['stellar_temp_k'] < 4000]
print(f"Planets around M-dwarfs: {len(m_dwarf_planets)}")
```

### Custom Analysis Functions

```python
def find_earth_twins(data, max_radius_diff=0.2, max_mass_diff=0.2):
    """Find planets most similar to Earth."""
    earth_twins = data[
        (abs(data['planet_radius_earth'] - 1.0) < max_radius_diff) &
        (abs(data['planet_mass_earth'] - 1.0) < max_mass_diff) &
        (data['in_habitable_zone'] == True)
    ].sort_values('stellar_distance_pc')
    return earth_twins

earth_twins = find_earth_twins(data)
print(f"Earth twin candidates: {len(earth_twins)}")
print(earth_twins[['planet_name', 'planet_radius_earth', 'planet_mass_earth']])
```

### Export Filtered Results

```python
# Save potentially habitable planets to separate file
habitable = data[data['in_habitable_zone'] == True]
habitable.to_csv('habitable_exoplanets.csv', index=False)

# Save only key columns
key_data = data[['planet_name', 'host_star', 'planet_type', 
                 'stellar_distance_pc', 'discovery_year']]
key_data.to_csv('exoplanet_summary.csv', index=False)
```

---

## Advanced Usage

### Custom Data Source Integration

```python
class ExoplanetDataCollector:
    # ... existing code ...
    
    def fetch_custom_source(self):
        """Add your own data source."""
        import requests
        
        # Example: fetch from custom API
        url = "https://your-custom-source.com/api/exoplanets"
        response = requests.get(url)
        
        if response.status_code == 200:
            custom_data = pd.DataFrame(response.json())
            # Map to unified schema
            # ... mapping code ...
            return custom_data
        return None
```

### Custom Visualizations

```python
import plotly.express as px
import matplotlib.pyplot as plt

# Custom scatter plot
fig = px.scatter(data, 
                x='stellar_temp_k', 
                y='planet_radius_earth',
                color='discovery_method',
                size='planet_mass_earth',
                hover_data=['planet_name'],
                log_y=True,
                title='Planet Radius vs Stellar Temperature')
fig.show()

# Custom histogram
plt.figure(figsize=(12, 6))
plt.hist(data['equilibrium_temp_k'].dropna(), bins=50, alpha=0.7)
plt.xlabel('Equilibrium Temperature (K)')
plt.ylabel('Count')
plt.title('Distribution of Planet Temperatures')
plt.axvline(x=288, color='r', linestyle='--', label='Earth (288 K)')
plt.legend()
plt.savefig('custom_temperature_histogram.png', dpi=300)
```

### Batch Processing

```python
# Process multiple datasets
import glob

csv_files = glob.glob('data/*.csv')
all_data = []

for file in csv_files:
    df = pd.read_csv(file)
    all_data.append(df)

combined = pd.concat(all_data, ignore_index=True)
combined = combined.drop_duplicates(subset=['planet_name'])
print(f"Combined {len(all_data)} files into {len(combined)} unique planets")
```

### Automated Reports

```python
def generate_monthly_report(data, output_dir='reports'):
    """Generate automated report with latest data."""
    from datetime import datetime
    import os
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate statistics
    stats = {
        'report_date': datetime.now().strftime('%Y-%m-%d'),
        'total_planets': len(data),
        'new_this_month': len(data[data['discovery_year'] == datetime.now().year]),
        'habitable_zone': len(data[data['in_habitable_zone'] == True]),
        'detection_methods': data['discovery_method'].value_counts().to_dict()
    }
    
    # Save statistics
    import json
    with open(f'{output_dir}/report_{stats["report_date"]}.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    # Generate visualizations
    viz = ExoplanetVisualizer(data)
    viz.generate_all_visualizations()
    
    print(f"Report generated in {output_dir}/")
    return stats

report = generate_monthly_report(data)
```

---

## Troubleshooting

### Network Issues

If you get connection errors:
```python
# Use demo data instead
collector.load_demo_data()
```

### Missing Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Or install individually
pip install pandas numpy matplotlib seaborn plotly astroquery astropy
```

### Data Quality

```python
# Check for missing values
print(data.isnull().sum())

# Fill missing values if needed
data['planet_mass_earth'].fillna(data['planet_mass_earth'].median(), inplace=True)

# Remove incomplete rows
clean_data = data.dropna(subset=['planet_radius_earth', 'planet_mass_earth'])
```

---

## Tips and Best Practices

1. **Always save your data** after collection to avoid re-downloading
2. **Use demo data** for testing visualizations without network access
3. **Filter before visualizing** large datasets for better performance
4. **Check data completeness** for the fields you need before analysis
5. **Export results** of interesting queries for future reference
6. **Combine multiple sources** for the most complete dataset
7. **Update regularly** - new exoplanets are discovered frequently!

---

## Additional Resources

- NASA Exoplanet Archive: https://exoplanetarchive.ipac.caltech.edu/
- EU Exoplanet Catalogue: http://exoplanet.eu/
- Open Exoplanet Catalogue: http://www.openexoplanetcatalogue.com/
- Exoplanet Data Explorer: http://exoplanets.org/

For more help, see the main [README.md](README.md) or open an issue on GitHub.
