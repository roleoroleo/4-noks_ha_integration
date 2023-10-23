"""The 4-noks component."""

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (CONF_NAME)
from homeassistant.core import HomeAssistant

from .common import get_dat
from .const import (CONF_SERIAL, DOMAIN)

PLATFORMS = ["sensor", "switch"]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up 4-noks from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data[CONF_SERIAL]
    hass.data[DOMAIN][entry.data[CONF_NAME]] = entry.data[CONF_NAME]

    hass.config_entries.async_update_entry(entry, data=entry.data)

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
