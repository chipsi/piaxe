This Raspberry Pi mining HAT is based on the [BitAxe Ultra 1.3](https://github.com/skot/bitaxe
) (with BM1366) design.

Update: Miner is running stable 🥳

<img src="https://github.com/shufps/piaxe-miner/assets/3079832/bde9dbb6-5687-4b4b-b0a8-7d4b83432937" width="500px"/>



Changes to BitAxe Ultra
=======================

- powered by 12V and
- added TVS diode and fuses
- revised buck switching regulator circuit
- revised heatsink
- removed like DAC (only fixed 1.2V on PiAxe), current measurement, fan PWM controller, additional testpoints
- smallest components have 0805 size for easier manual assembly
- LM75 compatible temperature sensor under the heatsink

Installation
=============

- add to `/boot/config.txt`:
```
dtoverlay=pwm
```

- enable `serial` and `I2C` via `raspi-config`

If you want to use Influx and Grafana you need docker too:

```bash
$ curl -sSL https://get.docker.com | sh
```

Python:
```bash
# install pip3
$ sudo apt install python3-pip

# install libraries
$ for lib in pyserial rpi_hardware_pwm smbus influxdb-client pytz; do pip3 install $lib; done

# install i2c-tools
$ sudo apt install i2c-tools
```


Mining Client
=============

<img src="https://github.com/shufps/piaxe-miner/assets/3079832/8d34ec13-15bd-4dd4-abd3-9588c823c494" width="400px"/>

Stratum Mining Client:<br>
https://github.com/shufps/piaxe-miner
