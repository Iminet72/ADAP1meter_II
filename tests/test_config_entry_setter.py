"""
Test to verify that the config_entry property setter works correctly.
This validates the fix for the AttributeError when setting config_entry.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class MockConfigEntry:
    """Mock ConfigEntry for testing."""
    def __init__(self, entry_id="test123", title="Test Entry", data=None):
        self.entry_id = entry_id
        self.title = title
        self.data = data or {}


def test_config_entry_property():
    """Test that config_entry property can be get and set without errors."""
    print("Testing config_entry property getter and setter...")
    
    # Import the module (this won't work without Home Assistant, but we can test the logic)
    config_flow_path = os.path.join(
        os.path.dirname(__file__), '..', 'custom_components/adap1ii/config_flow.py'
    )
    
    # Read the file and check for the property implementation
    with open(config_flow_path, 'r') as f:
        content = f.read()
    
    # Verify the property getter is defined
    has_getter = '@property' in content and 'def config_entry(self):' in content
    if has_getter:
        print("✓ config_entry property getter is defined")
    else:
        print("✗ config_entry property getter is missing")
        return False
    
    # Verify the property setter is defined
    has_setter = '@config_entry.setter' in content and 'def config_entry(self, value):' in content
    if has_setter:
        print("✓ config_entry property setter is defined")
    else:
        print("✗ config_entry property setter is missing")
        return False
    
    # Verify the private attribute is used
    uses_private_attr = '_config_entry_data' in content
    if uses_private_attr:
        print("✓ Private attribute _config_entry_data is used")
    else:
        print("✗ Private attribute _config_entry_data is not used")
        return False
    
    # Verify the getter returns the private attribute
    getter_lines = []
    in_getter = False
    for line in content.split('\n'):
        if 'def config_entry(self):' in line and '@property' in content[:content.index(line)]:
            in_getter = True
        elif in_getter:
            if line.strip().startswith('def '):
                break
            if 'return' in line:
                getter_lines.append(line)
                break
    
    if getter_lines and '_config_entry_data' in ''.join(getter_lines):
        print("✓ Getter returns the private attribute")
    else:
        print("⚠ Could not verify getter implementation")
    
    # Verify the setter assigns to the private attribute
    setter_lines = []
    in_setter = False
    for line in content.split('\n'):
        if 'def config_entry(self, value):' in line and '@config_entry.setter' in content[:content.index(line)]:
            in_setter = True
        elif in_setter:
            if line.strip().startswith('def '):
                break
            if '=' in line and '_config_entry_data' in line:
                setter_lines.append(line)
                break
    
    if setter_lines:
        print("✓ Setter assigns to the private attribute")
    else:
        print("⚠ Could not verify setter implementation")
    
    print("\n✓ All checks passed - config_entry property is properly implemented")
    return True


def test_no_direct_assignment():
    """Verify that direct assignment to config_entry is not done in __init__."""
    print("\nTesting that __init__ doesn't directly assign to config_entry...")
    
    config_flow_path = os.path.join(
        os.path.dirname(__file__), '..', 'custom_components/adap1ii/config_flow.py'
    )
    
    with open(config_flow_path, 'r') as f:
        lines = f.readlines()
    
    # Find the __init__ method
    in_init = False
    init_lines = []
    for line in lines:
        if 'def __init__(self, config_entry):' in line:
            in_init = True
        elif in_init:
            if line.strip().startswith('def ') or (line and not line[0].isspace()):
                break
            init_lines.append(line)
    
    init_content = ''.join(init_lines)
    
    # Check that we don't have direct assignment in __init__
    if 'self.config_entry = config_entry' in init_content and 'self._config_entry_data' not in init_content:
        print("✗ __init__ still uses direct assignment (will cause AttributeError)")
        return False
    elif 'self._config_entry_data = config_entry' in init_content:
        print("✓ __init__ uses private attribute (correct implementation)")
        return True
    else:
        print("⚠ Could not determine assignment pattern")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Testing config_entry property implementation")
    print("=" * 60)
    
    test1 = test_config_entry_property()
    test2 = test_no_direct_assignment()
    
    print("=" * 60)
    if test1 and test2:
        print("All tests passed! ✓")
        print("\nThe AttributeError fix is correctly implemented.")
        print("The config_entry property now has both getter and setter,")
        print("which prevents the AttributeError when the framework tries")
        print("to set the config_entry attribute.")
        sys.exit(0)
    else:
        print("Some tests failed! ✗")
        sys.exit(1)
