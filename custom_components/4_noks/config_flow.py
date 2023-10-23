"""Config flow for 4-noks integration."""

import csv
import logging
import socket

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import (CONF_HOST, CONF_NAME)
from io import StringIO

from .common import get_inf
from .const import (CONF_INTERVAL, CONF_SERIAL, DEFAULT_BRAND, DEFAULT_HOST,
                    DEFAULT_INTERVAL, DOMAIN)

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = {
    vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
    vol.Required(CONF_INTERVAL, default=DEFAULT_INTERVAL): int,
}


class FourNoksFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a 4-noks config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            interval = user_input[CONF_INTERVAL]

            response = await self.hass.async_add_executor_job(get_inf, user_input)
            if response is None:
                _LOGGER.error("Unable to get configuration from device %s", host)
                errors["base"] = "cannot_get_conf"
            else:
                try:
                    serial_number = response["SN"]
                except KeyError:
                    serial_number = None

                if serial_number is not None:
                    user_input[CONF_NAME] = DEFAULT_BRAND + "_" + serial_number
                    user_input[CONF_SERIAL] = serial_number
                else:
                    _LOGGER.error("Unable to get serial number from device %s", host)
                    errors["base"] = "cannot_get_serial"

                if not errors:
                    await self.async_set_unique_id(user_input[CONF_SERIAL])
                    self._abort_if_unique_id_configured()

                    for entry in self._async_current_entries():
                        if entry.data[CONF_SERIAL] == user_input[CONF_SERIAL]:
                            _LOGGER.error("Device already configured: %s", host)
                            return self.async_abort(reason="already_configured")

                    return self.async_create_entry(
                        title=user_input[CONF_NAME],
                        data=user_input
                    )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(DATA_SCHEMA),
            errors=errors,
        )
