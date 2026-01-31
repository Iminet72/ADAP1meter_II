"""
Test to verify OptionsFlowHandler initialization works correctly.
This test doesn't require Home Assistant to be installed.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_options_flow_handler_init():
    """Test that Ada12OptionsFlowHandler can be initialized with correct pattern."""
    # We can't fully test this without Home Assistant, but we can verify the class structure
    
    # Read the config_flow.py file using absolute path
    config_flow_path = os.path.join(
        os.path.dirname(__file__), '..', 'custom_components/adap1ii/config_flow.py'
    )
    with open(config_flow_path, 'r') as f:
        content = f.read()
    
    # Check that the __init__ method has the correct structure
    # It should:
    # 1. Call super().__init__() without arguments
    # 2. Assign self.config_entry = config_entry
    
    init_section = None
    lines = content.split('\n')
    in_init = False
    init_lines = []
    
    for line in lines:
        if 'def __init__(self, config_entry):' in line:
            in_init = True
        elif in_init:
            if line.strip().startswith('def ') or (line and not line[0].isspace()):
                break
            init_lines.append(line)
    
    init_content = '\n'.join(init_lines)
    
    # Verify super().__init__() is called without arguments
    if 'super().__init__()' in init_content:
        print("✓ super().__init__() is called correctly (without config_entry)")
    else:
        print("✗ super().__init__() is not called correctly")
        if 'super().__init__(config_entry)' in init_content:
            print("  ERROR: super().__init__(config_entry) found - this will cause TypeError!")
        return False
    
    # Verify config_entry is stored (either directly or in private attribute)
    if 'self._config_entry_data = config_entry' in init_content:
        print("✓ config_entry is stored in private attribute (recommended)")
    elif 'self.config_entry = config_entry' in init_content:
        print("✓ self.config_entry is assigned directly")
    else:
        print("✗ config_entry is not stored")
        return False
    
    # Check if there's a property with setter defined
    property_lines = []
    in_property = False
    for i, line in enumerate(lines):
        if '@property' in line and i < len(lines) - 1 and 'config_entry' in lines[i+1]:
            in_property = True
        elif in_property:
            if line.strip().startswith('@') or (line.strip().startswith('def ') and 'config_entry' not in line):
                in_property = False
            else:
                property_lines.append(line)
    
    if '@config_entry.setter' in content:
        print("✓ config_entry property has a setter (prevents AttributeError)")
    
    print("✓ Ada12OptionsFlowHandler.__init__ has correct structure")
    return True


if __name__ == "__main__":
    print("Testing Ada12OptionsFlowHandler initialization...")
    print("-" * 60)
    
    if test_options_flow_handler_init():
        print("-" * 60)
        print("Test passed! ✓")
        sys.exit(0)
    else:
        print("-" * 60)
        print("Test failed! ✗")
        sys.exit(1)
