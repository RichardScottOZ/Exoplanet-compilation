"""
Simple tests for the Exoplanet Database Compilation system

These tests validate basic functionality without requiring network access.
"""

import sys
import pandas as pd
import numpy as np
from demo_data_generator import generate_demo_data
from exoplanet_data_sources import ExoplanetDataCollector
from exoplanet_visualizations import ExoplanetVisualizer


def test_demo_data_generation():
    """Test that demo data can be generated."""
    print("Testing demo data generation...")
    data = generate_demo_data(50)
    
    assert len(data) == 50, "Should generate 50 planets"
    assert 'planet_name' in data.columns, "Should have planet_name column"
    assert 'discovery_method' in data.columns, "Should have discovery_method column"
    assert data['planet_radius_jupiter'].notna().all(), "All planets should have radius"
    
    print("✓ Demo data generation works correctly")
    return True


def test_data_collection():
    """Test data collection and processing."""
    print("\nTesting data collection...")
    collector = ExoplanetDataCollector()
    
    # Load demo data
    collector.load_demo_data()
    assert collector.nasa_data is not None, "Demo data should load"
    assert len(collector.nasa_data) > 0, "Demo data should not be empty"
    
    # Create unified schema
    unified = collector.create_unified_schema()
    assert unified is not None, "Should create unified schema"
    assert len(unified) > 0, "Unified data should not be empty"
    
    # Enrich data
    enriched = collector.enrich_data()
    assert 'planet_radius_earth' in enriched.columns, "Should add Earth radius"
    assert 'planet_type' in enriched.columns, "Should classify planet types"
    assert 'in_habitable_zone' in enriched.columns, "Should calculate habitable zone"
    
    print("✓ Data collection and processing works correctly")
    return True


def test_data_enrichment():
    """Test derived column calculations."""
    print("\nTesting data enrichment...")
    data = generate_demo_data(20)
    collector = ExoplanetDataCollector()
    collector.nasa_data = data
    collector.create_unified_schema()
    enriched = collector.enrich_data()
    
    # Check conversions
    jupiter_to_earth_radius = 11.209
    first_radius_earth = enriched['planet_radius_earth'].iloc[0]
    first_radius_jup = enriched['planet_radius_jupiter'].iloc[0]
    expected = first_radius_jup * jupiter_to_earth_radius
    # Simple numerical comparison with tolerance
    assert abs(first_radius_earth - expected) < 0.01, \
        f"Radius conversion failed: {first_radius_earth} != {expected}"
    
    # Check planet type classification
    types = enriched['planet_type'].unique()
    expected_types = ['Rocky (Earth-like)', 'Super-Earth', 'Neptune-like', 'Jupiter-like', 'Unknown']
    assert all(t in expected_types for t in types), "Planet types should be valid"
    
    # Check habitable zone calculation
    assert 'hz_inner_au' in enriched.columns, "Should calculate HZ inner boundary"
    assert 'hz_outer_au' in enriched.columns, "Should calculate HZ outer boundary"
    
    print("✓ Data enrichment works correctly")
    return True


def test_statistics():
    """Test statistics generation."""
    print("\nTesting statistics...")
    collector = ExoplanetDataCollector()
    collector.load_demo_data()
    collector.create_unified_schema()
    collector.enrich_data()
    
    # This should not crash
    collector.get_statistics()
    
    print("✓ Statistics generation works correctly")
    return True


def test_data_export():
    """Test data saving."""
    print("\nTesting data export...")
    import os
    import tempfile
    
    collector = ExoplanetDataCollector()
    collector.load_demo_data()
    collector.create_unified_schema()
    collector.enrich_data()
    
    # Save to temp file (cross-platform)
    temp_dir = tempfile.gettempdir()
    test_file = os.path.join(temp_dir, 'test_exoplanet_data.csv')
    collector.save_data(test_file)
    
    # Verify files exist
    assert os.path.exists(test_file), "CSV file should be created"
    assert os.path.exists(test_file.replace('.csv', '.json')), "JSON file should be created"
    
    # Verify data can be loaded
    loaded_data = pd.read_csv(test_file)
    assert len(loaded_data) > 0, "Loaded data should not be empty"
    assert 'planet_name' in loaded_data.columns, "Should have planet_name column"
    
    # Cleanup
    os.remove(test_file)
    os.remove(test_file.replace('.csv', '.json'))
    
    print("✓ Data export works correctly")
    return True


def test_visualization_initialization():
    """Test visualization system initialization."""
    print("\nTesting visualization initialization...")
    data = generate_demo_data(30)
    collector = ExoplanetDataCollector()
    collector.nasa_data = data
    collector.create_unified_schema()
    enriched = collector.enrich_data()
    
    # Initialize visualizer
    viz = ExoplanetVisualizer(enriched)
    assert viz.data is not None, "Visualizer should have data"
    assert len(viz.data) > 0, "Visualizer data should not be empty"
    
    print("✓ Visualization initialization works correctly")
    return True


def test_end_to_end():
    """Test complete end-to-end workflow."""
    print("\nTesting end-to-end workflow...")
    import os
    import tempfile
    
    # Full pipeline
    collector = ExoplanetDataCollector()
    collector.load_demo_data()
    collector.create_unified_schema()
    collector.enrich_data()
    
    # Save data (cross-platform temp dir)
    temp_dir = tempfile.gettempdir()
    test_file = os.path.join(temp_dir, 'test_e2e_data.csv')
    collector.save_data(test_file)
    
    # Load and visualize
    data = pd.read_csv(test_file)
    viz = ExoplanetVisualizer(data)
    
    # Generate one visualization to test
    fig = viz.plot_3d_galaxy_view(save_html=False)
    assert fig is not None, "Should create visualization"
    
    # Cleanup
    os.remove(test_file)
    os.remove(test_file.replace('.csv', '.json'))
    
    print("✓ End-to-end workflow works correctly")
    return True


def run_all_tests():
    """Run all tests."""
    print("="*70)
    print("RUNNING EXOPLANET COMPILATION SYSTEM TESTS")
    print("="*70)
    
    tests = [
        test_demo_data_generation,
        test_data_collection,
        test_data_enrichment,
        test_statistics,
        test_data_export,
        test_visualization_initialization,
        test_end_to_end
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
