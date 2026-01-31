# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2024-01-31

### ⚠️ BREAKING CHANGES

- **Domain Renamed:** The integration domain has been changed from `bhsoft` to `adap1ii`
- This is a breaking change that affects existing installations
- See [MIGRATION.md](MIGRATION.md) for detailed migration instructions

### Added

- **Automatic Migration:** Added migration shim that automatically migrates config entries from old domain to new domain
- **Migration Documentation:** Comprehensive migration guide in MIGRATION.md
- **Migration Logging:** Detailed logging during the migration process to help users track progress
- **Duplicate Prevention:** Migration shim checks for existing entries to prevent duplicates
- **Structure Tests:** Added automated tests to verify integration structure and syntax

### Changed

- Integration domain changed from `bhsoft` to `adap1ii`
- Updated all internal references to use new domain
- Updated README.md with migration instructions and warnings
- Updated LICENSE copyright line
- Cleaned up unused variables in sensor.py

### Migration Instructions

**IMPORTANT: Backup your Home Assistant configuration before updating!**

1. Install the update through HACS or your installation method
2. Restart Home Assistant
3. The migration shim will automatically detect old entries and create new ones
4. Verify your devices and sensors work correctly under the new `adap1ii` integration
5. Check Home Assistant logs for migration summary
6. After verification, manually remove old `bhsoft` config entries

For detailed instructions and troubleshooting, see [MIGRATION.md](MIGRATION.md).

### Technical Details

The migration works as follows:
- Both `bhsoft` (shim) and `adap1ii` (new integration) are present in the update
- On startup, the shim's `async_setup` function runs and detects old config entries
- For each old entry, the shim creates a new entry under `adap1ii` with identical configuration
- The shim compares URLs and host:port combinations to prevent duplicate migrations
- Detailed logs are written to help users understand what happened
- Old entries are NOT automatically deleted (users should verify and delete manually)

### Security

- No security vulnerabilities detected by CodeQL analysis
- No external dependencies added
- Migration shim uses only Home Assistant's built-in config entry APIs

---

## [1.0.2] - Previous Version

Previous version with `bhsoft` domain name.

For older changelog entries, please refer to git history.
