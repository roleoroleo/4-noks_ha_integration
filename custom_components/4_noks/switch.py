"""Support for switches from 4-noks devices."""

import logging

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_NAME
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .common import set_rel
from .const import (CONF_SERIAL, DEFAULT_BRAND, DOMAIN)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the 4-noks switches from a config entry."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]["COORDINATOR"]
    if coordinator is None:
        _LOGGER.error("Unable to get coordinator")
        return

    entities = [
        FourNOKSSwitch(coordinator, config_entry, "Relay state"),
    ]

    async_add_entities(entities)


class FourNOKSSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a 4-noks Switch."""

    def __init__(self, coordinator, config, switch_name):
        """Initialize the device."""
        super().__init__(coordinator)
        self._config_data = config.data
        self._device_name = config.data[CONF_NAME]
        self._serial = config.data[CONF_SERIAL]

        self._basename = switch_name
        self._fullname = self._device_name + "_" + self._basename
        self._name = self._device_name + "_" + self._basename.lower().replace(' ', '_')
        self._unique_id = self._name

        if switch_name == "Relay state":
            self._attr_unique_id = self._device_name + "_swre"
            self._attr_icon = "mdi:radiator"

        self._attr_is_on = False
        if self.coordinator.data is not None:
            rel_state = self.coordinator.data[self._basename]
            if rel_state == "1":
                self._attr_is_on = True
            else:
                self._attr_is_on = False

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch"""
        rel = await self.hass.async_add_executor_job(set_rel, self._config_data, 0)
        if rel is None:
            _LOGGER.error("Unable to set relay")
            return

        await self.coordinator.async_refresh()
        if self.coordinator.data is not None:
            rel_state = self.coordinator.data[self._basename]
            if rel_state == "1":
                self._attr_is_on = True
            else:
                self._attr_is_on = False
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch"""
        rel = await self.hass.async_add_executor_job(set_rel, self._config_data, 1)
        if rel is None:
            _LOGGER.error("Unable to set relay")
            return

        await self.coordinator.async_refresh()
        if self.coordinator.data is not None:
            rel_state = self.coordinator.data[self._basename]
            if rel_state == "1":
                self._attr_is_on = True
            else:
                self._attr_is_on = False
            self.async_write_ha_state()

    def update(self) -> None:
        """Refresh a relay's state."""
        if self.coordinator.data is not None:
            rel_state = self.coordinator.data[self._basename]
            if rel_state == "1":
                self._attr_is_on = True
            else:
                self._attr_is_on = False

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def brand(self):
        """Camera brand."""
        return DEFAULT_BRAND

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the device."""
        return self._unique_id

    @property
    def device_info(self):
        """Return device specific attributes."""
        return {
            "name": self._device_name,
            "identifiers": {(DOMAIN, self._serial)},
            "manufacturer": DEFAULT_BRAND,
            "model": DOMAIN,
        }
