"""
Exoplanet Data Source Integration Module

This module provides unified access to multiple exoplanet databases:
- NASA Exoplanet Archive
- EU Exoplanet Catalogue (exoplanet.eu)
- Open Exoplanet Catalogue
- Exoplanet Orbit Database
- TEPCat (Transiting Extrasolar Planet Catalogue)
"""

import pandas as pd
import numpy as np
import requests
try:
    from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
except ImportError:
    # Fallback for older astroquery versions
    from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive
from astropy.time import Time
import warnings
warnings.filterwarnings('ignore')


class ExoplanetDataCollector:
    """Main class for collecting and integrating exoplanet data from multiple sources."""
    
    def __init__(self):
        self.nasa_data = None
        self.eu_data = None
        self.oec_data = None
        self.combined_data = None
        
    def load_demo_data(self):
        """
        Load demo data for testing when network access is unavailable.
        """
        print("Loading demo data...")
        try:
            from demo_data_generator import generate_demo_data
            demo_df = generate_demo_data(100)
            
            # Treat demo data as NASA data for processing
            self.nasa_data = demo_df
            print(f"Successfully loaded {len(demo_df)} demo planets")
            return demo_df
        except Exception as e:
            print(f"Error loading demo data: {e}")
            return None
    
    def fetch_nasa_exoplanet_archive(self):
        """
        Fetch data from NASA Exoplanet Archive.
        Uses the Planetary Systems Composite Parameters table.
        """
        print("Fetching NASA Exoplanet Archive data...")
        try:
            # Get the composite planet data table
            self.nasa_data = NasaExoplanetArchive.query_criteria(
                table="pscomppars",
                select="*"
            ).to_pandas()
            
            print(f"Successfully fetched {len(self.nasa_data)} planets from NASA")
            return self.nasa_data
        except Exception as e:
            print(f"Error fetching NASA data: {e}")
            return None
    
    def fetch_eu_exoplanet_catalogue(self):
        """
        Fetch data from the EU Exoplanet Catalogue (exoplanet.eu).
        """
        print("Fetching EU Exoplanet Catalogue data...")
        try:
            # EU catalogue CSV export URL
            url = "http://exoplanet.eu/catalog/csv"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                # Save temporarily and read as CSV
                from io import StringIO
                self.eu_data = pd.read_csv(StringIO(response.text))
                print(f"Successfully fetched {len(self.eu_data)} planets from EU catalogue")
                return self.eu_data
            else:
                print(f"Failed to fetch EU data: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching EU data: {e}")
            return None
    
    def fetch_open_exoplanet_catalogue(self):
        """
        Fetch data from the Open Exoplanet Catalogue GitHub repository.
        """
        print("Fetching Open Exoplanet Catalogue data...")
        try:
            # OEC provides data in various formats; we'll use their CSV export
            url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.csv"
            self.oec_data = pd.read_csv(url, compression='gzip', error_bad_lines=False)
            print(f"Successfully fetched {len(self.oec_data)} systems from OEC")
            return self.oec_data
        except Exception as e:
            print(f"Error fetching OEC data: {e}")
            # Alternative: use a simplified approach
            return None
    
    def create_unified_schema(self):
        """
        Create a unified schema from all data sources.
        Maps common fields across different databases.
        """
        print("Creating unified data schema...")
        
        unified_data = []
        
        # Process NASA data
        if self.nasa_data is not None and len(self.nasa_data) > 0:
            # Check if this is demo data or real NASA data
            is_demo = 'data_source' in self.nasa_data.columns
            
            for _, row in self.nasa_data.iterrows():
                if is_demo:
                    # Demo data already has the right format
                    unified_data.append(dict(row))
                else:
                    # Real NASA data needs mapping
                    unified_data.append({
                        'planet_name': row.get('pl_name', ''),
                        'host_star': row.get('hostname', ''),
                        'discovery_method': row.get('discoverymethod', ''),
                        'discovery_year': row.get('disc_year', np.nan),
                        'orbital_period_days': row.get('pl_orbper', np.nan),
                        'planet_radius_jupiter': row.get('pl_radj', np.nan),
                        'planet_mass_jupiter': row.get('pl_bmassj', np.nan),
                        'orbital_distance_au': row.get('pl_orbsmax', np.nan),
                        'eccentricity': row.get('pl_orbeccen', np.nan),
                        'equilibrium_temp_k': row.get('pl_eqt', np.nan),
                        'stellar_distance_pc': row.get('sy_dist', np.nan),
                        'stellar_mass_solar': row.get('st_mass', np.nan),
                        'stellar_radius_solar': row.get('st_rad', np.nan),
                        'stellar_temp_k': row.get('st_teff', np.nan),
                        'ra_deg': row.get('ra', np.nan),
                        'dec_deg': row.get('dec', np.nan),
                        'data_source': 'NASA Exoplanet Archive'
                    })
        
        # Process EU data
        if self.eu_data is not None and len(self.eu_data) > 0:
            # Map EU column names to unified schema
            for _, row in self.eu_data.iterrows():
                # Only add if not already in unified data (avoid duplicates)
                planet_name = row.get('name', row.get('# name', ''))
                if not any(p['planet_name'] == planet_name for p in unified_data):
                    unified_data.append({
                        'planet_name': planet_name,
                        'host_star': row.get('star_name', ''),
                        'discovery_method': row.get('detection_type', ''),
                        'discovery_year': row.get('discovered', np.nan),
                        'orbital_period_days': row.get('orbital_period', np.nan),
                        'planet_radius_jupiter': row.get('radius', np.nan),
                        'planet_mass_jupiter': row.get('mass', np.nan),
                        'orbital_distance_au': row.get('semi_major_axis', np.nan),
                        'eccentricity': row.get('eccentricity', np.nan),
                        'equilibrium_temp_k': row.get('temp_calculated', np.nan),
                        'stellar_distance_pc': row.get('star_distance', np.nan),
                        'stellar_mass_solar': row.get('star_mass', np.nan),
                        'stellar_radius_solar': row.get('star_radius', np.nan),
                        'stellar_temp_k': row.get('star_teff', np.nan),
                        'ra_deg': row.get('ra', np.nan),
                        'dec_deg': row.get('dec', np.nan),
                        'data_source': 'EU Exoplanet Catalogue'
                    })
        
        self.combined_data = pd.DataFrame(unified_data)
        print(f"Created unified dataset with {len(self.combined_data)} planets")
        
        return self.combined_data
    
    def enrich_data(self):
        """
        Add derived columns and enrich the dataset with calculations.
        """
        if self.combined_data is None or len(self.combined_data) == 0:
            print("No data to enrich. Run create_unified_schema() first.")
            return self.combined_data
        
        print("Enriching dataset with derived values...")
        
        # Convert radius to Earth radii
        if 'planet_radius_jupiter' in self.combined_data.columns:
            self.combined_data['planet_radius_earth'] = (
                self.combined_data['planet_radius_jupiter'] * 11.209  # Jupiter radius in Earth radii
            )
        
        # Convert mass to Earth masses
        if 'planet_mass_jupiter' in self.combined_data.columns:
            self.combined_data['planet_mass_earth'] = (
                self.combined_data['planet_mass_jupiter'] * 317.8  # Jupiter mass in Earth masses
            )
        
        # Calculate density (if we have both mass and radius)
        if 'planet_mass_jupiter' in self.combined_data.columns and 'planet_radius_jupiter' in self.combined_data.columns:
            volume_jupiter = (4/3) * np.pi * (self.combined_data['planet_radius_jupiter'] ** 3)
            self.combined_data['density_g_cm3'] = np.where(
                (self.combined_data['planet_mass_jupiter'] > 0) & 
                (self.combined_data['planet_radius_jupiter'] > 0),
                self.combined_data['planet_mass_jupiter'] * 1.898e27 / (volume_jupiter * 1.4313e27),
                np.nan
            )
        
        # Classify planets by size
        def classify_planet_type(radius_earth):
            if pd.isna(radius_earth):
                return 'Unknown'
            elif radius_earth < 1.5:
                return 'Rocky (Earth-like)'
            elif radius_earth < 2.0:
                return 'Super-Earth'
            elif radius_earth < 6.0:
                return 'Neptune-like'
            else:
                return 'Jupiter-like'
        
        if 'planet_radius_earth' in self.combined_data.columns:
            self.combined_data['planet_type'] = self.combined_data['planet_radius_earth'].apply(
                classify_planet_type
            )
        
        # Estimate habitable zone distance (simplified)
        # HZ varies with stellar luminosity, roughly 0.95-1.37 AU for Sun-like stars
        if 'stellar_radius_solar' in self.combined_data.columns and 'stellar_temp_k' in self.combined_data.columns:
            stellar_luminosity = (self.combined_data['stellar_radius_solar'] ** 2) * \
                                ((self.combined_data['stellar_temp_k'] / 5778) ** 4)
            self.combined_data['hz_inner_au'] = 0.95 * np.sqrt(stellar_luminosity)
            self.combined_data['hz_outer_au'] = 1.37 * np.sqrt(stellar_luminosity)
        
        # Check if in habitable zone
        if 'orbital_distance_au' in self.combined_data.columns and 'hz_inner_au' in self.combined_data.columns:
            self.combined_data['in_habitable_zone'] = (
                (self.combined_data['orbital_distance_au'] >= self.combined_data['hz_inner_au']) &
                (self.combined_data['orbital_distance_au'] <= self.combined_data['hz_outer_au'])
            )
        
        # Calculate galactic coordinates (simplified - would need proper coordinate transformation)
        # For now, just convert RA/Dec to cartesian
        if 'ra_deg' in self.combined_data.columns and 'dec_deg' in self.combined_data.columns:
            dist = self.combined_data['stellar_distance_pc'].fillna(100)  # Default to 100 pc if unknown
            ra_rad = np.radians(self.combined_data['ra_deg'])
            dec_rad = np.radians(self.combined_data['dec_deg'])
            
            self.combined_data['x_pc'] = dist * np.cos(dec_rad) * np.cos(ra_rad)
            self.combined_data['y_pc'] = dist * np.cos(dec_rad) * np.sin(ra_rad)
            self.combined_data['z_pc'] = dist * np.sin(dec_rad)
        
        print("Data enrichment complete!")
        
        return self.combined_data
    
    def save_data(self, filename='exoplanet_combined_data.csv'):
        """Save the combined dataset to a CSV file."""
        if self.combined_data is None:
            print("No data to save.")
            return
        
        self.combined_data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        
        # Also save a JSON version for web applications
        json_filename = filename.replace('.csv', '.json')
        self.combined_data.to_json(json_filename, orient='records', indent=2)
        print(f"Data also saved to {json_filename}")
    
    def get_statistics(self):
        """Generate summary statistics about the combined dataset."""
        if self.combined_data is None:
            print("No data available.")
            return
        
        print("\n" + "="*60)
        print("EXOPLANET DATABASE STATISTICS")
        print("="*60)
        
        print(f"\nTotal planets: {len(self.combined_data)}")
        
        if 'data_source' in self.combined_data.columns:
            print("\nPlanets by source:")
            print(self.combined_data['data_source'].value_counts())
        
        if 'discovery_method' in self.combined_data.columns:
            print("\nPlanets by discovery method:")
            print(self.combined_data['discovery_method'].value_counts().head(10))
        
        if 'discovery_year' in self.combined_data.columns:
            print("\nDiscovery year range:")
            print(f"  First: {self.combined_data['discovery_year'].min()}")
            print(f"  Latest: {self.combined_data['discovery_year'].max()}")
        
        if 'planet_type' in self.combined_data.columns:
            print("\nPlanets by type:")
            print(self.combined_data['planet_type'].value_counts())
        
        if 'in_habitable_zone' in self.combined_data.columns:
            hz_count = self.combined_data['in_habitable_zone'].sum()
            print(f"\nPlanets in habitable zone: {hz_count}")
        
        print("\nData completeness:")
        key_columns = ['planet_radius_jupiter', 'planet_mass_jupiter', 
                      'orbital_period_days', 'orbital_distance_au']
        for col in key_columns:
            if col in self.combined_data.columns:
                completeness = (1 - self.combined_data[col].isna().sum() / len(self.combined_data)) * 100
                print(f"  {col}: {completeness:.1f}%")
        
        print("="*60 + "\n")


def main():
    """Main function to demonstrate data collection."""
    collector = ExoplanetDataCollector()
    
    # Try to fetch from all sources, fall back to demo data if needed
    success = False
    
    # Try NASA
    nasa_result = collector.fetch_nasa_exoplanet_archive()
    if nasa_result is not None and len(nasa_result) > 0:
        success = True
    
    # Try EU
    eu_result = collector.fetch_eu_exoplanet_catalogue()
    if eu_result is not None and len(eu_result) > 0:
        success = True
    
    # If no data collected, use demo data
    if not success:
        print("\n" + "!"*70)
        print("! No network access or API errors - using demo data instead")
        print("!"*70 + "\n")
        collector.load_demo_data()
    
    # Create unified dataset
    collector.create_unified_schema()
    
    # Enrich with derived values
    collector.enrich_data()
    
    # Show statistics
    collector.get_statistics()
    
    # Save data
    collector.save_data()
    
    return collector


if __name__ == "__main__":
    collector = main()
