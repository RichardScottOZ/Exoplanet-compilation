#!/usr/bin/env python3
"""
Command-line interface for Exoplanet Database Compilation

Usage:
    python main.py --collect      # Collect data from all sources
    python main.py --visualize    # Generate visualizations
    python main.py --all          # Do both (default)
    python main.py --stats        # Show statistics only
"""

import sys
import argparse
from exoplanet_data_sources import ExoplanetDataCollector
from exoplanet_visualizations import ExoplanetVisualizer
import pandas as pd


def collect_data(output_file='exoplanet_combined_data.csv'):
    """Collect and integrate exoplanet data."""
    print("\n" + "="*70)
    print(" EXOPLANET DATA COLLECTION")
    print("="*70 + "\n")
    
    collector = ExoplanetDataCollector()
    
    # Fetch from all sources
    print("Step 1: Fetching data from NASA Exoplanet Archive...")
    collector.fetch_nasa_exoplanet_archive()
    
    print("\nStep 2: Fetching data from EU Exoplanet Catalogue...")
    collector.fetch_eu_exoplanet_catalogue()
    
    # Note: Uncomment to add more sources
    # print("\nStep 3: Fetching data from Open Exoplanet Catalogue...")
    # collector.fetch_open_exoplanet_catalogue()
    
    print("\nStep 3: Creating unified schema...")
    collector.create_unified_schema()
    
    print("\nStep 4: Enriching data with derived values...")
    collector.enrich_data()
    
    print("\nStep 5: Saving data...")
    collector.save_data(output_file)
    
    print("\nStep 6: Generating statistics...")
    collector.get_statistics()
    
    print("\n" + "="*70)
    print(" DATA COLLECTION COMPLETE!")
    print("="*70 + "\n")
    
    return collector.combined_data


def generate_visualizations(data_file='exoplanet_combined_data.csv'):
    """Generate all visualizations."""
    print("\n" + "="*70)
    print(" EXOPLANET VISUALIZATION GENERATION")
    print("="*70 + "\n")
    
    try:
        data = pd.read_csv(data_file)
        print(f"Loaded {len(data)} planets from {data_file}\n")
    except FileNotFoundError:
        print(f"Error: {data_file} not found!")
        print("Please run with --collect first to collect data.")
        return
    
    viz = ExoplanetVisualizer(data)
    viz.generate_all_visualizations()
    
    print("\n" + "="*70)
    print(" VISUALIZATION GENERATION COMPLETE!")
    print("="*70 + "\n")
    print("Generated files:")
    print("  - exoplanet_3d_view.html")
    print("  - exoplanet_mass_radius.html")
    print("  - exoplanet_discovery_timeline.html")
    print("  - exoplanet_habitable_zone.html")
    print("  - exoplanet_dashboard.html")
    print("  - detection_methods.png")
    print("  - stellar_properties.png")
    print("\nOpen the HTML files in your web browser for interactive visualizations!")
    print()


def show_statistics(data_file='exoplanet_combined_data.csv'):
    """Show statistics only."""
    try:
        data = pd.read_csv(data_file)
        collector = ExoplanetDataCollector()
        collector.combined_data = data
        collector.get_statistics()
    except FileNotFoundError:
        print(f"Error: {data_file} not found!")
        print("Please run with --collect first to collect data.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Exoplanet Database Compilation & Visualization Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py                    # Run full pipeline (collect + visualize)
  python main.py --collect          # Collect data only
  python main.py --visualize        # Generate visualizations only
  python main.py --stats            # Show statistics only
  python main.py --all              # Run full pipeline (same as no args)
        '''
    )
    
    parser.add_argument('--collect', action='store_true',
                       help='Collect data from all sources')
    parser.add_argument('--visualize', action='store_true',
                       help='Generate visualizations')
    parser.add_argument('--stats', action='store_true',
                       help='Show statistics only')
    parser.add_argument('--all', action='store_true',
                       help='Run full pipeline (collect + visualize)')
    parser.add_argument('--output', default='exoplanet_combined_data.csv',
                       help='Output file for combined data (default: exoplanet_combined_data.csv)')
    
    args = parser.parse_args()
    
    # Default to --all if no arguments
    if not any([args.collect, args.visualize, args.stats, args.all]):
        args.all = True
    
    # Execute requested operations
    if args.stats:
        show_statistics(args.output)
    
    elif args.collect and args.visualize:
        collect_data(args.output)
        generate_visualizations(args.output)
    
    elif args.all:
        collect_data(args.output)
        generate_visualizations(args.output)
    
    elif args.collect:
        collect_data(args.output)
    
    elif args.visualize:
        generate_visualizations(args.output)
    
    print("\n✅ All done! Check the generated files for results.\n")


if __name__ == "__main__":
    main()
