"""Support for collecting sensors from 4-noks devices."""

import datetime
import logging
import time

from homeassistant.components.sensor import (SensorDeviceClass,
                                             SensorEntity,
                                             SensorStateClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (CONF_HOST, CONF_NAME)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import event
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .common import get_dat
from .const import (CONF_SERIAL, DEFAULT_BRAND, DOMAIN)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up energy sensors."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]["COORDINATOR"]
    if coordinator is None:
        _LOGGER.error("Unable to get coordinator")
        return

    # Get a list of sensors and units of measurement
    dat = await hass.async_add_executor_job(get_dat, config_entry.data, True)
    if dat is None:
        return

    entities = []
    for name, um in dat.items():
        entities.append(FourNOKSSensor(coordinator, config_entry, name, um))

    async_add_entities(entities)


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
            self._device_class = SensorDeviceClass.POWER
            self._state_class = SensorStateClass.MEASUREMENT
        elif (self._um.lower() == "kwh"):
            self._device_class = SensorDeviceClass.ENERGY
            self._state_class = SensorStateClass.TOTAL_INCREASING
        elif (self._um.lower() == "dd/mm/yyyy hh:mm:ss"):
            self._um = ""
            self._device_class = SensorDeviceClass.DATE
#            self._device_class = None
            self._state_class = None
        else:
            self._device_class = None
            self._state_class = None

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
    def state_class(self):
        """Return state class."""
        return self._state_class

    @property
    def device_info(self):
        """Return device specific attributes."""
        return {
            "name": self._device_name,
            "identifiers": {(DOMAIN, self._serial)},
            "manufacturer": DEFAULT_BRAND,
            "model": DOMAIN,
        }
