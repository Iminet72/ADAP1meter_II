import asyncio
import logging
import time
import async_timeout
from datetime import timedelta

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .product_config import get_product_sensors, get_product_name

from homeassistant.components.sensor import SensorEntity, SensorStateClass, SensorDeviceClass

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=10)

# The meter regularly answers {"error": "No v2 data available yet"} while it refreshes its P1
# telegram, and its WiFi drops the odd request. Retry briefly, then keep showing the last good
# reading for a short while instead of turning every sensor unknown/unavailable for a poll.
REQUEST_TIMEOUT = 5  # s per attempt
RETRIES = 2  # extra attempts after the first one
RETRY_DELAY = 1.0  # s between attempts
HOLD_LAST_GOOD = 60  # s a stale reading may be served before the sensors go unavailable


async def async_setup_entry(hass, config_entry, async_add_entities):
    config_data = {**config_entry.data, **config_entry.options}
    prefix = config_data.get("prefix", "")
    product_type = config_data.get("product_type", "default_type")
    
    # ------------------------
    # URL logika
    # ------------------------
    url = config_data.get("url")
    if not url:
        host = config_data.get("host", "okosvillanyora.local")
        port = config_data.get("port", 8989)
        url = f"http://{host}:{port}/json"
    
    device_id = f"ada_p1_meter_{url}_{product_type}"

    product_sensors = get_product_sensors(product_type)
    product_name = get_product_name(product_type)

    session = async_get_clientsession(hass)
    last_good = {"data": None, "ts": 0.0}

    async def fetch_once():
        async with async_timeout.timeout(REQUEST_TIMEOUT):
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json(content_type=None)
        if not isinstance(data, dict):
            raise ValueError("unexpected response")
        if "error" in data:  # e.g. "No v2 data available yet"
            raise ValueError(data["error"])
        return data

    async def async_update_data():
        last_err = None
        for attempt in range(1 + RETRIES):
            try:
                data = await fetch_once()
                last_good["data"], last_good["ts"] = data, time.monotonic()
                return data
            except Exception as err:  # noqa: BLE001 - any failure is retried the same way
                last_err = err
                if attempt < RETRIES:
                    await asyncio.sleep(RETRY_DELAY)

        age = time.monotonic() - last_good["ts"]
        if last_good["data"] is not None and age < HOLD_LAST_GOOD:
            _LOGGER.debug("%s: %s, keeping the reading from %.0f s ago", url, last_err, age)
            return last_good["data"]
        raise UpdateFailed(f"Error fetching data from {url}: {last_err}") from last_err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{prefix} {product_name} coordinator",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    # Not async_config_entry_first_refresh(): raising ConfigEntryNotReady from a forwarded
    # platform is not retried by HA, so a meter that was offline at startup stayed unavailable
    # until a manual reload. The entities are added either way and recover on the next poll.
    await coordinator.async_refresh()

    sensors = []
    for sensor_key, sensor_config in product_sensors.items():
        unique_id = f"{url}_{product_type}_{sensor_key}"
        sensors.append(
            Ada12Sensor(
                coordinator=coordinator,
                product_type=product_type,
                sensor_key=sensor_key,
                sensor_config=sensor_config,
                unique_id=unique_id,
                prefix=prefix,
                name=f"{prefix} {product_name} {sensor_config['friendly_name']}",
                device_id=device_id,
            )
        )

    async_add_entities(sensors)


class Ada12Sensor(CoordinatorEntity, SensorEntity):
    ENERGY_SENSORS = ["active_import_energy_total", "active_export_energy_total"]

    def __init__(self, coordinator, product_type, sensor_key, sensor_config, unique_id, prefix, name, device_id):
        super().__init__(coordinator)
        self._product_type = product_type
        self._sensor_key = sensor_key
        self._sensor_config = sensor_config
        self._unique_id = unique_id
        self._prefix = prefix
        self._name = name
        self._device_id = device_id
        self._attr_icon = sensor_config["icon"]
        self._extra_attrs = {"uid": unique_id}

        # Energy panelhez szükséges beállítás
        state_class = sensor_config.get("state_class")
        if state_class == "total_increasing" or sensor_key in self.ENERGY_SENSORS:
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
            self._attr_native_unit_of_measurement = "kWh"
        elif state_class == "measurement":
            self._attr_state_class = SensorStateClass.MEASUREMENT
            unit = sensor_config.get("unit", "")
            self._attr_native_unit_of_measurement = unit
            if unit == "kW":
                self._attr_device_class = SensorDeviceClass.POWER
        elif sensor_config.get("unit"):
            self._attr_native_unit_of_measurement = sensor_config["unit"]

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def device_info(self):
        return {
            "identifiers": {(self._device_id,)},  
            "name": f"{self._prefix} {self._product_type}",
            "manufacturer": "ADA",
            "model": self._product_type,
        }      
            
    @property
    def native_value(self):
        data = self.coordinator.data or {}
        if self._sensor_key not in data:
            return None
        return data[self._sensor_key]

    @property
    def extra_state_attributes(self):
        return self._extra_attrs

