from homeassistant import config_entries
import voluptuous as vol
from homeassistant.core import callback
import logging
import aiohttp
import async_timeout

from .product_config import get_product_list, get_product_name, get_product_sensors, PRODUCT_CONFIGS

DOMAIN = "adap1ii"
_LOGGER = logging.getLogger(__name__)


class Ada12ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        product_options = {
            key: f"{conf['name']} (host: {conf['host']}, port: {conf['default_port']})"
            for key, conf in PRODUCT_CONFIGS.items()
        }

        if user_input is not None:
            product_type = user_input.get("product_type", "ada12")
            prefix = user_input.get("prefix", "")
            url = user_input.get("url")
            host = user_input.get("host")
            port = user_input.get("port", 8989)

            # Ha nincs teljes URL, építsük össze host+port alapján
            if not url:
                if not host:
                    host = PRODUCT_CONFIGS.get(product_type, {}).get("host", "okosvillanyora.local")
                if not port:
                    port = PRODUCT_CONFIGS.get(product_type, {}).get("default_port", 8989)
                url = f"http://{host}:{port}/json"

            # Próbáljunk csatlakozni a JSON-hoz és ellenőrizzük a szenzorokat
            try:
                async with aiohttp.ClientSession() as session:
                    async with async_timeout.timeout(10):
                        async with session.get(url) as response:
                            if response.status != 200:
                                raise Exception(f"HTTP {response.status}")
                            data = await response.json()

                # Ellenőrizzük, hogy legalább az egyik szenzor kulcs létezik
                expected_sensors = get_product_sensors(product_type)
                if not any(key in data for key in expected_sensors):
                    raise Exception("No expected sensors found in JSON")

                # Minden rendben, létrehozzuk az entry-t
                title = get_product_name(product_type)
                if prefix:
                    title = f"{prefix} {title}"
                return self.async_create_entry(title=title, data=user_input)

            except Exception as err:
                _LOGGER.error("Cannot connect to %s: %s", url, err)
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema({
            vol.Required("product_type", default="ada12"): vol.In(product_options),
            vol.Optional("prefix", default=""): str,
            vol.Optional("host", default=""): str,
            vol.Optional("port", default=8989): int,
            vol.Optional("url", default=""): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return Ada12OptionsFlowHandler(config_entry)


class Ada12OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        super().__init__()
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        product_options = dict(get_product_list())
        options_schema = vol.Schema({
            vol.Optional(
                "product_type", default=self.config_entry.data.get("product_type", "ada12")
            ): vol.In(product_options),
            vol.Optional("prefix", default=self.config_entry.data.get("prefix", "")): str,
            vol.Optional("host", default=self.config_entry.data.get("host", "")): str,
            vol.Optional("port", default=self.config_entry.data.get("port", 8989)): int,
            vol.Optional("url", default=self.config_entry.data.get("url", "")): str,
        })

        return self.async_show_form(step_id="init", data_schema=options_schema)
