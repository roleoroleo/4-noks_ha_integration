"""Support for collecting sensors from 4-noks devices."""

import async_timeout
import datetime
import logging
import time

from datetime import timedelta
from homeassistant.components import mqtt
from homeassistant.components.sensor import (DEVICE_CLASS_BATTERY,
                                             DEVICE_CLASS_ENERGY,
                                             DEVICE_CLASS_POWER,
                                             DEVICE_CLASS_TIMESTAMP,
                                             SensorEntity)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (CONF_HOST, CONF_NAME)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import event
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .common import get_dat
from .const import (CONF_SERIAL, DEFAULT_BRAND, DOMAIN)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry, async_add_entities):
    """Set up energy sensors."""

    async def async_update_data():
        """Fetch data from socket endpoint."""

        async with async_timeout.timeout(10):
            dat = await hass.async_add_executor_job(get_dat, config.data, False)
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
        update_interval=timedelta(seconds=60),
    )

    # Get a list of sensors and units of measurement
    dat = await hass.async_add_executor_job(get_dat, config.data, True)

    entities = []
    for name, um in dat.items():
        entities.append(FourNOKSSensor(coordinator, config, name, um))

    async_add_entities(entities)

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()


class FourNOKSSensor(CoordinatorEntity, SensorEntity):
    """Representation of a 4-noks sensor."""

    def __init__(self, coordinator, config, sensor_name, sensor_um):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_name = config.data[CONF_NAME]
        self._serial = config.data[CONF_SERIAL]

        self._basename = sensor_name
        self._fullname = self._device_name + "_" + self._basename
        self._name = self._device_name + "_" + self._basename.lower().replace(' ', '_')
        self._unique_id = self._name
        self._um = sensor_um
        if (self._um.lower() == "kw"):
            self._device_class = DEVICE_CLASS_POWER
        elif (self._um.lower() == "kwh"):
            self._device_class = DEVICE_CLASS_ENERGY
        elif (self._um.lower() == "dd/mm/yyyy hh:mm:ss"):
            self._um = ""
#            self._device_class = DEVICE_CLASS_TIMESTAMP
            self._device_class = None
        else:
            self._device_class = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def native_value(self):
        """Return the value of the sensor."""
        if self.coordinator.data is not None:
            return self.coordinator.data[self._basename]

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement of the sensor, if any."""
        return self._um

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not self.coordinator.last_update_success:
            return False

        return True

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

    @property
    def device_class(self):
        """Return the icon to use in the frontend."""
        return self._device_class

    @property
    def device_info(self):
        """Return device specific attributes."""
        return {
            "name": self._device_name,
            "identifiers": {(DOMAIN, self._serial)},
            "manufacturer": DEFAULT_BRAND,
            "model": DOMAIN,
        }
