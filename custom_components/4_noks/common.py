"""Common utils for 4-noks device."""

import csv
import logging
import socket

from datetime import timedelta
from io import StringIO

from homeassistant.const import CONF_HOST
from homeassistant.util import dt as dt_util

from .const import (
    DEFAULT_PORT,
    DOMAIN,
    TCP_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)


def get_inf(config):
    """Get system info from device."""
    host = config[CONF_HOST]
    error = False
    dict_inf = {}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TCP_TIMEOUT)
    try:
        s.connect((host, DEFAULT_PORT))
    except socket.error:
        _LOGGER.error("Failed to connect to device %s", host)
        error = True
    except OSError:
        _LOGGER.error("Failed to connect to device %s", host)
        error = True

    if error:
        return None

    try:
        s.sendall(b'@inf\n')
        data = s.recv(2048)
        s.close()
    except socket.error:
        _LOGGER.error("Failed to get status from device %s", host)
        error = True
    except OSError:
        _LOGGER.error("Failed to get status from device %s", host)
        error = True

    if error:
        s.close()
        return None

    try:
        f_inf = StringIO(data.decode())
        reader_inf = csv.reader(f_inf, delimiter='=')
    except csv.Error:
        _LOGGER.error("Unable to parse status from device %s", host)
        error = True

    if error:
        return None

    try:
        if reader_inf is not None:
            for row_inf in reader_inf:
                if (row_inf is not None) and (len(row_inf) >= 2):
                    dict_inf[row_inf[0]] = row_inf[1]
    except KeyError:
        _LOGGER.error("Unable to parse status from device %s", host)
        error = True

    if error:
        return None

    return dict_inf


def get_dat(config, um):
    """Get data from device."""
    host = config[CONF_HOST]
    error = False
    dict_dat = {}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TCP_TIMEOUT)
    try:
        s.connect((host, DEFAULT_PORT))
    except socket.error:
        _LOGGER.error("Failed to connect to device %s", host)
        error = True
    except OSError:
        _LOGGER.error("Failed to connect to device %s", host)
        error = True

    if error:
        return None

    try:
        s.sendall(b'@dat\n')
        data = s.recv(2048)
        s.close()
    except socket.error:
        _LOGGER.error("Failed to get data from device %s", host)
        error = True
    except OSError:
        _LOGGER.error("Failed to get data from device %s", host)
        error = True

    if error:
        s.close()
        return None

    try:
        f_dat = StringIO(data.decode())
        reader_dat = csv.reader(f_dat, delimiter=';')
    except csv.Error:
        _LOGGER.error("Unable to parse data from device %s", host)
        error = True

    if error:
        return None

    try:
        if reader_dat is not None:
            for row_dat in reader_dat:
                if (row_dat is not None) and (len(row_dat) >= 4):
                    if (row_dat[0] != "@DAT"):
                        if um:
                            dict_dat[row_dat[1]] = row_dat[3]
                        else:
                            dict_dat[row_dat[1]] = row_dat[2]
    except KeyError:
        _LOGGER.error("Unable to parse data from device %s", host)
        error = True

    if error:
        return None

    return dict_dat

def set_power_off_in_progress(hass, device_name):
    hass.data[DOMAIN][device_name + END_OF_POWER_OFF] = dt_util.utcnow() + timedelta(seconds=5)

def power_off_in_progress(hass, device_name):
    return (
        hass.data[DOMAIN][device_name + END_OF_POWER_OFF] is not None
        and hass.data[DOMAIN][device_name + END_OF_POWER_OFF] > dt_util.utcnow()
    )

def set_power_on_in_progress(hass, device_name):
    hass.data[DOMAIN][device_name + END_OF_POWER_ON] = dt_util.utcnow() + timedelta(seconds=5)

def power_on_in_progress(hass, device_name):
    return (
        hass.data[DOMAIN][device_name + END_OF_POWER_ON] is not None
        and hass.data[DOMAIN][device_name + END_OF_POWER_ON] > dt_util.utcnow()
    )
