"""The 4-noks component."""

import async_timeout
import asyncio
import logging

from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (CONF_NAME)
from homeassistant.core import HomeAssistant

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .common import get_dat
from .const import (CONF_INTERVAL, CONF_SERIAL, DOMAIN)

PLATFORMS = ["sensor", "switch"]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up 4-noks from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}
    hass.data[DOMAIN][entry.entry_id]["SERIAL"] = entry.data[CONF_SERIAL]
    hass.data[DOMAIN][entry.entry_id]["NAME"] = entry.data[CONF_NAME]

    interval = entry.data[CONF_INTERVAL]

    async def async_update_data():
        """Fetch data from socket endpoint."""

        async with async_timeout.timeout(10):
            dat = await hass.async_add_executor_job(get_dat, entry.data, False)
            if dat is None:
                _LOGGER.error("No data available")

        return dat

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name="4-noks sensor",
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=interval),
    )

    hass.data[DOMAIN][entry.entry_id]["COORDINATOR"] = coordinator

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

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
