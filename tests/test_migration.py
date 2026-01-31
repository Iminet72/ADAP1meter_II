"""
Simple test to verify migration shim can be imported and has correct structure.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_bhsoft_shim_imports():
    """Test that the bhsoft shim can be imported."""
    try:
        # Import the shim module
        from custom_components.bhsoft import __init__ as bhsoft_shim
        
        # Check that it has the required functions
        assert hasattr(bhsoft_shim, 'async_setup'), "async_setup function not found"
        assert hasattr(bhsoft_shim, 'async_setup_entry'), "async_setup_entry function not found"
        assert hasattr(bhsoft_shim, 'async_unload_entry'), "async_unload_entry function not found"
        
        # Check constants
        assert bhsoft_shim.DOMAIN == "bhsoft", "DOMAIN should be 'bhsoft'"
        assert bhsoft_shim.NEW_DOMAIN == "adap1ii", "NEW_DOMAIN should be 'adap1ii'"
        
        print("✓ bhsoft shim structure is correct")
        return True
    except Exception as e:
        print(f"✗ Failed to import or validate bhsoft shim: {e}")
        return False


def test_adap1ii_imports():
    """Test that the adap1ii integration can be imported."""
    try:
        # Import the new integration modules
        from custom_components.adap1ii import __init__ as adap1ii_init
        from custom_components.adap1ii import config_flow
        from custom_components.adap1ii import sensor
        from custom_components.adap1ii import product_config
        
        # Check domain constant
        assert adap1ii_init.DOMAIN == "adap1ii", "DOMAIN in __init__.py should be 'adap1ii'"
        assert config_flow.DOMAIN == "adap1ii", "DOMAIN in config_flow.py should be 'adap1ii'"
        
        print("✓ adap1ii integration structure is correct")
        return True
    except Exception as e:
        print(f"✗ Failed to import or validate adap1ii integration: {e}")
        return False


if __name__ == "__main__":
    print("Running migration tests...")
    print("-" * 60)
    
    test1 = test_bhsoft_shim_imports()
    test2 = test_adap1ii_imports()
    
    print("-" * 60)
    if test1 and test2:
        print("All tests passed! ✓")
        sys.exit(0)
    else:
        print("Some tests failed! ✗")
        sys.exit(1)
