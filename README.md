# ADA Family Meters Integration for Home Assistant V II adap1ii

![HACS Default](https://img.shields.io/badge/HACS-Default-orange.svg?style=flat-square)
![Home Assistant](https://img.shields.io/badge/Supports-Home%20Assistant-blue?style=flat-square)
![HACS Supported](https://img.shields.io/badge/HACS-Supported-41BDF5?style=flat-square)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green?style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)


This is a custom integration for [Home Assistant](https://www.home-assistant.io/) that provides sensor data from an ADA Meter, including total energy consumption, phase voltage, current, power factors, and more.

This is a modified version for easier handling, more devices can be managed with it, adapted to the new energy dashboard

You can find the original here:

(https://github.com/greenhess/adap1meter)

Thanks for Grennhess Kft

## ⚠️ Important: Domain Renamed (bhsoft → adap1ii)

**If you are upgrading from an older version**, please note that the integration domain has been changed from `bhsoft` to `adap1ii`.

### Automatic Migration

Good news! The migration is **automatic**:

1. **Backup your Home Assistant configuration** before updating (important!)
2. Install the update through HACS or your installation method
3. Restart Home Assistant
4. The migration shim will automatically create new config entries under the `adap1ii` domain
5. Verify your devices and sensors work correctly
6. After verification, you can safely remove the old `bhsoft` config entries

### Migration Details

- A migration shim is included that runs on startup
- Your existing configuration (host, port, settings) will be preserved
- Detailed migration logs will be written to help you track the process
- See [MIGRATION.md](MIGRATION.md) for complete migration guide and troubleshooting

## License

This project is licensed under the MIT License.

![ADA P1 Meter Icon](images/icon.png)
