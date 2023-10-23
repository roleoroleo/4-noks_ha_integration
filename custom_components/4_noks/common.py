"""Common utils for 4-noks device."""

import csv
import logging
import socket

from datetime import datetime, timedelta
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
                            if (row_dat[3] == "dd/mm/yyyy hh:mm:ss"):
                                rd2 = row_dat[2]
                                try:
                                    dict_dat[row_dat[1]] = datetime.strptime(row_dat[2], '%d/%m/%Y %H:%M:%S')
                                except:
                                    dict_dat[row_dat[1]] = datetime.strptime("01/01/1970 00:00:00", '%d/%m/%Y %H:%M:%S')
                                    _LOGGER.error("Unable to parse date/time from device %s", host)
                            else:
                                dict_dat[row_dat[1]] = row_dat[2]
    except KeyError:
        _LOGGER.error("Unable to parse data from device %s", host)
        error = True

    if error:
        return None

    return dict_dat

def set_rel(config, value):
    """Set relay."""
    host = config[CONF_HOST]
    error = False
    command = b'@rel 0 ' + str(value).encode() + b'\n'

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
        return False

    try:
        s.sendall(command)
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
        return False

    return True
