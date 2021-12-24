<p align="center">
        <a target="_blank" href="https://github.com/roleoroleo/4-noks_ha_integration/releases">
                <img src="https://img.shields.io/github/downloads/roleoroleo/4-noks_ha_integration/total.svg" alt="Releases Downloads">
        </a>
</p>

# 4-NOKS Home Assistant integration

## Overview
4-NOKS Home Assistant is a custom integration for 4-NOKS Elios4you devices
<br>

This integration is available from the Lovelace frontend without the need to configure the devices in the file configuration.yaml
The wizard will connect to your cam and will install all the entities detected from device, for example:
- Produced Power
- Produced Energy
- Produced Energy F1
- Produced Energy F2
- Produced Energy F3
- Consumed Power
- Consumed Energy
- Consumed Energy F1
- Consumed Energy F2
- Consumed Energy F3
- Bought Power
- Bought Energy
- Bought Energy F1
- Bought Energy F2
- Bought Energy F3
- Sold Power
- Sold Energy
- Sold Energy F1
- Sold Energy F2
- Sold Energy F3


## Installation
**(1)** Copy the  `custom_components` folder to your configuration directory.
It should look similar to this:
```
<config directory>/
|-- custom_components/
|   |-- 4_noks/
|       |-- translations/
|       |-- __init__.py
|       |-- common.py
|       |-- config_flow.py
|       |-- const.py
|       |-- manifest.json
|       |-- sensor.py
|       |-- strings.json
```
**(2)** Restart Home Assistant

**(3)** Configure device and entities:
- Go to Settings -> Integrations
- Click "Add Integration" in the lower-right corner
- Select "4-NOKS Elios4you" integration
<p align="center">
<img src="https://user-images.githubusercontent.com/39277388/147362185-a1ac9b12-9c23-4b27-b8e2-9100834fbdd6.png" width="400">
</p>

- Enter the host/ip of your device
<p align="center">
<img src="https://user-images.githubusercontent.com/39277388/147362239-4c43ee48-7e5d-404c-bf9c-8f8a3fa6e338.png" width="400">
</p>

- Confirm and wait for the wizard completion
- Set the "Area" if you need it
- Enjoy your device
<br><br>


## Acknowledgments
Special thanks to Davide Vertuani and his hacking story:
https://www.hackster.io/daveVertu/reverse-engineering-elios4you-photovoltaic-monitoring-device-458aa0


## Donation
If you like this project, you can buy me a beer :) 
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=JBYXDMR24FW7U&currency_code=EUR&source=url)

---
### DISCLAIMER
**I AM NOT RESPONSIBLE FOR ANY USE OR DAMAGE THIS SOFTWARE MAY CAUSE. THIS IS INTENDED FOR EDUCATIONAL PURPOSES ONLY. USE AT YOUR OWN RISK.**
