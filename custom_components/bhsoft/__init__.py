"""
Migration shim for bhsoft -> adap1ii domain rename.

This integration provides automatic migration of config entries from the old
'bhsoft' domain to the new 'adap1ii' domain.

IMPORTANT: This shim should remain in the repository to ensure smooth upgrades
for existing users. It will automatically detect old config entries and migrate
them to the new domain.

How it works:
1. On Home Assistant startup, this shim checks for existing config entries under 'bhsoft'
2. For each old entry found, it creates a corresponding entry under 'adap1ii'
3. The migration only runs once per old entry (checks for duplicates)
4. Detailed logs are written to help users understand the migration process
5. Old entries are NOT automatically removed - users should remove them manually
   after verifying the new entries work correctly

Migration is safe: it will not create duplicate entries if migration has already occurred.
"""

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

DOMAIN = "bhsoft"
NEW_DOMAIN = "adap1ii"

# Flag to track if migration has been attempted this session
_migration_attempted = False


async def async_setup(hass: HomeAssistant, config: dict):
    """
    Set up the migration shim.
    
    This runs on Home Assistant startup and performs the migration from
    bhsoft to adap1ii domain.
    """
    global _migration_attempted
    
    # Only attempt migration once per HA session
    if _migration_attempted:
        return True
    
    _migration_attempted = True
    
    _LOGGER.info(
        "=" * 80 + "\n"
        "bhsoft -> adap1ii Migration Shim\n"
        "=" * 80
    )
    
    # Get all config entries for the old domain
    old_entries = hass.config_entries.async_entries(DOMAIN)
    
    if not old_entries:
        _LOGGER.info("No old 'bhsoft' config entries found. Migration not needed.")
        return True
    
    _LOGGER.warning(
        f"Found {len(old_entries)} config entry(ies) under old domain 'bhsoft'. "
        "Starting migration to 'adap1ii'..."
    )
    
    # Get all existing entries for the new domain
    new_entries = hass.config_entries.async_entries(NEW_DOMAIN)
    
    migrated_count = 0
    skipped_count = 0
    
    for old_entry in old_entries:
        entry_data = old_entry.data
        entry_title = old_entry.title
        
        _LOGGER.info(f"Processing old entry: '{entry_title}' (entry_id: {old_entry.entry_id})")
        
        # Check if this entry has already been migrated by comparing data
        # We'll check if there's an entry with matching host/url
        already_migrated = False
        
        old_url = entry_data.get("url", "")
        old_host = entry_data.get("host", "")
        old_port = entry_data.get("port", "")
        
        for new_entry in new_entries:
            new_url = new_entry.data.get("url", "")
            new_host = new_entry.data.get("host", "")
            new_port = new_entry.data.get("port", "")
            
            # Check if URLs match or host+port match
            if old_url and new_url and old_url == new_url:
                already_migrated = True
                _LOGGER.info(
                    f"  → Entry already migrated (matching URL: {old_url}). Skipping."
                )
                break
            elif old_host and new_host and old_host == new_host and old_port == new_port:
                already_migrated = True
                _LOGGER.info(
                    f"  → Entry already migrated (matching host:port: {old_host}:{old_port}). Skipping."
                )
                break
        
        if already_migrated:
            skipped_count += 1
            continue
        
        # Create new entry under adap1ii domain
        try:
            _LOGGER.info(f"  → Creating new config entry under '{NEW_DOMAIN}' domain...")
            
            # Create the new entry with the same data and title
            new_entry = await hass.config_entries.flow.async_init(
                NEW_DOMAIN,
                context={"source": "import"},
                data=entry_data
            )
            
            migrated_count += 1
            _LOGGER.info(
                f"  ✓ Successfully created new entry for '{entry_title}' under '{NEW_DOMAIN}'"
            )
            
        except Exception as e:
            _LOGGER.error(
                f"  ✗ Failed to migrate entry '{entry_title}': {e}\n"
                f"    You may need to manually reconfigure this device under the new '{NEW_DOMAIN}' integration."
            )
    
    # Summary
    _LOGGER.warning(
        "=" * 80 + "\n"
        f"Migration Summary:\n"
        f"  - Total old entries found: {len(old_entries)}\n"
        f"  - Successfully migrated: {migrated_count}\n"
        f"  - Skipped (already migrated): {skipped_count}\n"
        f"  - Failed: {len(old_entries) - migrated_count - skipped_count}\n"
        "=" * 80 + "\n"
        "IMPORTANT: Please verify that your devices appear correctly under the new\n"
        f"'{NEW_DOMAIN}' integration. Once verified, you can safely remove the old\n"
        f"'{DOMAIN}' config entries from Home Assistant.\n"
        "=" * 80
    )
    
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """
    This should not be called as the shim doesn't create config entries.
    Just return True to avoid errors.
    """
    _LOGGER.warning(
        f"Config entry setup called on migration shim. This should not happen. "
        f"Entry: {entry.title} (ID: {entry.entry_id})"
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle unload of a config entry."""
    return True
