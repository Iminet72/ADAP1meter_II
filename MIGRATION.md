# Migration Guide: bhsoft → adap1ii

## Overview

The ADA Family Meters integration has been renamed from **bhsoft** to **adap1ii**. This is a breaking change that requires migration of your existing configuration.

**Good News:** The migration process is **automatic**! A migration shim has been included to make the transition as smooth as possible.

## What Changed?

- **Integration Domain:** `bhsoft` → `adap1ii`
- **Custom Component Directory:** `custom_components/bhsoft/` → `custom_components/adap1ii/`
- All internal references and constants have been updated

## Automatic Migration

### How It Works

1. When you install the updated version, both `bhsoft` (migration shim) and `adap1ii` (new integration) will be present
2. On Home Assistant restart, the migration shim automatically:
   - Detects existing config entries under the old `bhsoft` domain
   - Creates equivalent config entries under the new `adap1ii` domain
   - Preserves all your settings (host, port, prefix, product type, etc.)
   - Logs detailed information about the migration process

### Migration Steps

1. **Backup First** (IMPORTANT!)
   - Create a full backup of your Home Assistant configuration
   - You can use Home Assistant's built-in backup feature
   - This ensures you can restore if anything goes wrong

2. **Install the Update**
   - Update the integration through HACS or your installation method
   - The update includes both the new `adap1ii` integration and the migration shim

3. **Restart Home Assistant**
   - After installation, restart Home Assistant
   - The migration will run automatically during startup

4. **Check the Logs**
   - Open Home Assistant logs (Settings → System → Logs)
   - Look for messages from the `bhsoft` migration shim
   - You should see a summary of the migration:
     ```
     ================================================================================
     Migration Summary:
       - Total old entries found: X
       - Successfully migrated: X
       - Skipped (already migrated): X
       - Failed: 0
     ================================================================================
     ```

5. **Verify Your Devices**
   - Go to Settings → Devices & Services
   - Look for your ADA meters under the new `ADA Family Meters` integration (domain: adap1ii)
   - Verify that all your sensors are working correctly
   - Check your energy dashboard if you use it

6. **Remove Old Entries (After Verification)**
   - Once you've confirmed everything works with the new integration
   - You can safely remove the old `bhsoft` entries
   - Go to Settings → Devices & Services
   - Find the old "ADA Family Meters VII (Migration Shim)" entries
   - Click on each entry and select "Delete"
   - This step is optional but recommended to avoid confusion

## Troubleshooting

### Migration Didn't Happen

If the migration doesn't occur automatically:

1. Check Home Assistant logs for errors
2. Ensure both `bhsoft` and `adap1ii` directories exist in `custom_components/`
3. Try restarting Home Assistant again
4. If still not working, you may need to manually reconfigure:
   - Add the integration again using Settings → Devices & Services → Add Integration
   - Search for "ADA Family Meters"
   - Configure with the same settings you used before

### Duplicate Entries

The migration shim is designed to prevent duplicates by checking:
- Matching URLs
- Matching host + port combinations

If you see duplicates:
- Keep the entries under `adap1ii` (the new integration)
- Remove the entries under `bhsoft` (the old integration)

### Sensors Not Working

If sensors aren't working after migration:

1. Check that the device configuration is correct
2. Verify network connectivity to your ADA meter
3. Check Home Assistant logs for connection errors
4. If needed, delete and re-add the integration manually

## Manual Migration (If Needed)

If automatic migration fails or you prefer to do it manually:

1. Note down your current configuration:
   - Host/IP address
   - Port
   - Product type (ada12, adaone, adabridge, adapziote02)
   - Prefix (if any)
   - Custom URL (if any)

2. Remove old integration:
   - Go to Settings → Devices & Services
   - Find your ADA meter under "bhsoft"
   - Click and select "Delete"

3. Add new integration:
   - Go to Settings → Devices & Services → Add Integration
   - Search for "ADA Family Meters"
   - Configure with your noted settings

## Energy Dashboard

If you use the Home Assistant Energy Dashboard:

- After migration, you may need to update your energy dashboard configuration
- The sensor entity IDs will have changed (domain prefix changes from `bhsoft` to `adap1ii`)
- Go to Settings → Dashboards → Energy
- Update any references to old sensors with the new ones

## Support

If you encounter any issues during migration:

1. Check the [GitHub Issues](https://github.com/Iminet72/ADAP1meter_II/issues)
2. Create a new issue with:
   - Home Assistant version
   - Integration version
   - Relevant log entries
   - Description of the problem

## Why This Change?

The domain was renamed to better reflect the integration's purpose and to align with naming conventions. The `adap1ii` name represents "ADA P1 Integration II" (version 2).
