"""
Demo data generator for Exoplanet Compilation

Creates sample exoplanet data for demonstration and testing purposes
when network access is unavailable.
"""

import pandas as pd
import numpy as np


def generate_demo_data(num_planets=100):
    """
    Generate realistic sample exoplanet data.
    
    Parameters:
    -----------
    num_planets : int
        Number of planets to generate (default: 100)
    
    Returns:
    --------
    pandas.DataFrame
        Sample exoplanet data
    """
    np.random.seed(42)  # For reproducibility
    
    # Famous real exoplanets to include
    famous_planets = [
        {
            'planet_name': 'Proxima Centauri b',
            'host_star': 'Proxima Centauri',
            'discovery_method': 'Radial Velocity',
            'discovery_year': 2016,
            'orbital_period_days': 11.186,
            'planet_radius_jupiter': 0.099,  # ~1.1 Earth radii
            'planet_mass_jupiter': 0.004,    # ~1.3 Earth masses
            'orbital_distance_au': 0.0485,
            'eccentricity': 0.02,
            'equilibrium_temp_k': 234,
            'stellar_distance_pc': 1.3,
            'stellar_mass_solar': 0.12,
            'stellar_radius_solar': 0.154,
            'stellar_temp_k': 3042,
            'ra_deg': 217.4,
            'dec_deg': -62.7,
            'data_source': 'Demo Data'
        },
        {
            'planet_name': 'TRAPPIST-1e',
            'host_star': 'TRAPPIST-1',
            'discovery_method': 'Transit',
            'discovery_year': 2017,
            'orbital_period_days': 6.1,
            'planet_radius_jupiter': 0.083,  # ~0.92 Earth radii
            'planet_mass_jupiter': 0.002,    # ~0.77 Earth masses
            'orbital_distance_au': 0.028,
            'eccentricity': 0.0,
            'equilibrium_temp_k': 246,
            'stellar_distance_pc': 12.5,
            'stellar_mass_solar': 0.089,
            'stellar_radius_solar': 0.121,
            'stellar_temp_k': 2566,
            'ra_deg': 346.6,
            'dec_deg': -5.0,
            'data_source': 'Demo Data'
        },
        {
            'planet_name': 'Kepler-452b',
            'host_star': 'Kepler-452',
            'discovery_method': 'Transit',
            'discovery_year': 2015,
            'orbital_period_days': 384.8,
            'planet_radius_jupiter': 0.142,  # ~1.6 Earth radii
            'planet_mass_jupiter': 0.016,    # ~5 Earth masses
            'orbital_distance_au': 1.046,
            'eccentricity': 0.0,
            'equilibrium_temp_k': 265,
            'stellar_distance_pc': 430,
            'stellar_mass_solar': 1.04,
            'stellar_radius_solar': 1.11,
            'stellar_temp_k': 5757,
            'ra_deg': 292.9,
            'dec_deg': 44.3,
            'data_source': 'Demo Data'
        },
        {
            'planet_name': '51 Pegasi b',
            'host_star': '51 Pegasi',
            'discovery_method': 'Radial Velocity',
            'discovery_year': 1995,
            'orbital_period_days': 4.23,
            'planet_radius_jupiter': 1.2,
            'planet_mass_jupiter': 0.47,
            'orbital_distance_au': 0.0527,
            'eccentricity': 0.013,
            'equilibrium_temp_k': 1284,
            'stellar_distance_pc': 15.4,
            'stellar_mass_solar': 1.11,
            'stellar_radius_solar': 1.24,
            'stellar_temp_k': 5793,
            'ra_deg': 344.4,
            'dec_deg': 20.8,
            'data_source': 'Demo Data'
        },
        {
            'planet_name': 'HD 189733 b',
            'host_star': 'HD 189733',
            'discovery_method': 'Transit',
            'discovery_year': 2005,
            'orbital_period_days': 2.22,
            'planet_radius_jupiter': 1.14,
            'planet_mass_jupiter': 1.13,
            'orbital_distance_au': 0.031,
            'eccentricity': 0.0,
            'equilibrium_temp_k': 1201,
            'stellar_distance_pc': 19.8,
            'stellar_mass_solar': 0.82,
            'stellar_radius_solar': 0.76,
            'stellar_temp_k': 4875,
            'ra_deg': 300.2,
            'dec_deg': 22.7,
            'data_source': 'Demo Data'
        }
    ]
    
    # Generate additional random planets
    detection_methods = ['Transit', 'Radial Velocity', 'Direct Imaging', 'Microlensing', 'Transit Timing Variations']
    
    random_planets = []
    for i in range(num_planets - len(famous_planets)):
        # Generate random but realistic values
        method = np.random.choice(detection_methods, p=[0.75, 0.15, 0.05, 0.03, 0.02])
        year = np.random.randint(1995, 2024)
        
        # Planet properties (log-normal distributions for more realistic values)
        radius_jup = np.random.lognormal(-1.0, 1.5)  # Mostly smaller planets
        mass_jup = np.random.lognormal(-1.5, 1.5)
        orbital_period = np.random.lognormal(1.0, 2.0)
        orbital_distance = (orbital_period / 365.25) ** (2/3)  # Kepler's 3rd law approximation
        
        # Stellar properties
        stellar_mass = np.random.lognormal(0.0, 0.3)  # Mostly Sun-like
        stellar_radius = stellar_mass ** 0.8  # Mass-radius relation
        stellar_temp = 5778 * (stellar_mass ** 0.5)  # Approximate
        stellar_distance = np.random.lognormal(3.0, 1.5)  # Distance in parsecs
        
        # Calculate equilibrium temperature
        stellar_luminosity = (stellar_radius ** 2) * ((stellar_temp / 5778) ** 4)
        eq_temp = 279 * (stellar_luminosity ** 0.25) / (orbital_distance ** 0.5)
        
        # Random sky position
        ra = np.random.uniform(0, 360)
        dec = np.random.uniform(-90, 90)
        
        random_planets.append({
            'planet_name': f'Demo Planet {i+1:03d}',
            'host_star': f'Demo Star {i+1:03d}',
            'discovery_method': method,
            'discovery_year': year,
            'orbital_period_days': orbital_period,
            'planet_radius_jupiter': radius_jup,
            'planet_mass_jupiter': mass_jup,
            'orbital_distance_au': orbital_distance,
            'eccentricity': np.random.beta(1, 5),  # Most orbits are circular
            'equilibrium_temp_k': eq_temp,
            'stellar_distance_pc': stellar_distance,
            'stellar_mass_solar': stellar_mass,
            'stellar_radius_solar': stellar_radius,
            'stellar_temp_k': stellar_temp,
            'ra_deg': ra,
            'dec_deg': dec,
            'data_source': 'Demo Data'
        })
    
    # Combine famous and random planets
    all_planets = famous_planets + random_planets
    
    # Create DataFrame
    df = pd.DataFrame(all_planets)
    
    return df


def save_demo_data(filename='demo_exoplanet_data.csv'):
    """Generate and save demo data."""
    print("Generating demo exoplanet data...")
    data = generate_demo_data(100)
    
    data.to_csv(filename, index=False)
    print(f"Saved {len(data)} demo planets to {filename}")
    
    # Also save JSON version
    json_filename = filename.replace('.csv', '.json')
    data.to_json(json_filename, orient='records', indent=2)
    print(f"Also saved to {json_filename}")
    
    return data


if __name__ == "__main__":
    data = save_demo_data()
    
    print("\nDemo data statistics:")
    print(f"  Total planets: {len(data)}")
    print(f"  Detection methods: {data['discovery_method'].nunique()}")
    print(f"  Year range: {data['discovery_year'].min():.0f} - {data['discovery_year'].max():.0f}")
    print(f"\nSample planets:")
    print(data[['planet_name', 'discovery_method', 'planet_radius_jupiter']].head(10))
