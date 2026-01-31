"""
Test to verify the structure without importing Home Assistant dependencies.
"""
import os
import json
import ast

def test_file_structure():
    """Test that all required files exist."""
    print("Checking file structure...")
    
    required_files = [
        'custom_components/adap1ii/__init__.py',
        'custom_components/adap1ii/config_flow.py',
        'custom_components/adap1ii/manifest.json',
        'custom_components/adap1ii/sensor.py',
        'custom_components/adap1ii/product_config.py',
        'custom_components/bhsoft/__init__.py',
        'custom_components/bhsoft/manifest.json',
        'MIGRATION.md',
        'README.md',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING!")
            all_exist = False
    
    return all_exist


def test_domain_constants():
    """Test that DOMAIN constants are correct in Python files."""
    print("\nChecking DOMAIN constants...")
    
    # Check adap1ii files
    with open('custom_components/adap1ii/__init__.py', 'r') as f:
        content = f.read()
        if 'DOMAIN = "adap1ii"' in content:
            print('  ✓ adap1ii/__init__.py has correct DOMAIN')
        else:
            print('  ✗ adap1ii/__init__.py DOMAIN is incorrect!')
            return False
    
    with open('custom_components/adap1ii/config_flow.py', 'r') as f:
        content = f.read()
        if 'DOMAIN = "adap1ii"' in content:
            print('  ✓ adap1ii/config_flow.py has correct DOMAIN')
        else:
            print('  ✗ adap1ii/config_flow.py DOMAIN is incorrect!')
            return False
    
    # Check bhsoft shim
    with open('custom_components/bhsoft/__init__.py', 'r') as f:
        content = f.read()
        if 'DOMAIN = "bhsoft"' in content and 'NEW_DOMAIN = "adap1ii"' in content:
            print('  ✓ bhsoft/__init__.py has correct DOMAIN and NEW_DOMAIN')
        else:
            print('  ✗ bhsoft/__init__.py DOMAIN constants are incorrect!')
            return False
    
    return True


def test_manifest_files():
    """Test that manifest.json files are valid and have correct domains."""
    print("\nChecking manifest.json files...")
    
    # Check adap1ii manifest
    with open('custom_components/adap1ii/manifest.json', 'r') as f:
        manifest = json.load(f)
        if manifest.get('domain') == 'adap1ii':
            print('  ✓ adap1ii/manifest.json has correct domain')
        else:
            print(f'  ✗ adap1ii/manifest.json domain is {manifest.get("domain")}, expected "adap1ii"!')
            return False
    
    # Check bhsoft manifest
    with open('custom_components/bhsoft/manifest.json', 'r') as f:
        manifest = json.load(f)
        if manifest.get('domain') == 'bhsoft':
            print('  ✓ bhsoft/manifest.json has correct domain')
        else:
            print(f'  ✗ bhsoft/manifest.json domain is {manifest.get("domain")}, expected "bhsoft"!')
            return False
        
        # Check that config_flow is disabled for shim
        if manifest.get('config_flow') == False:
            print('  ✓ bhsoft/manifest.json has config_flow disabled (correct for shim)')
        else:
            print('  ! bhsoft/manifest.json has config_flow enabled (should be disabled for shim)')
    
    return True


def test_python_syntax():
    """Test that all Python files have valid syntax."""
    print("\nChecking Python syntax...")
    
    python_files = [
        'custom_components/adap1ii/__init__.py',
        'custom_components/adap1ii/config_flow.py',
        'custom_components/adap1ii/sensor.py',
        'custom_components/adap1ii/product_config.py',
        'custom_components/bhsoft/__init__.py',
    ]
    
    all_valid = True
    for file in python_files:
        try:
            with open(file, 'r') as f:
                ast.parse(f.read())
            print(f'  ✓ {file} - syntax OK')
        except SyntaxError as e:
            print(f'  ✗ {file} - SYNTAX ERROR: {e}')
            all_valid = False
    
    return all_valid


if __name__ == "__main__":
    print("=" * 60)
    print("Running structure and syntax tests...")
    print("=" * 60)
    
    test1 = test_file_structure()
    test2 = test_domain_constants()
    test3 = test_manifest_files()
    test4 = test_python_syntax()
    
    print("\n" + "=" * 60)
    if test1 and test2 and test3 and test4:
        print("All tests passed! ✓")
        exit(0)
    else:
        print("Some tests failed! ✗")
        exit(1)
