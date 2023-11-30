This Raspberry Pi mining HAT is based on the [BitAxe Ultra 1.3](https://github.com/skot/bitaxe
) (with BM1366) design.

Update: Miner is running stable 🥳


![image](https://github.com/shufps/piaxe/assets/3079832/1b79eda2-acb0-4a86-ad00-c1af6b7e4b8b)




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

- enable PWM and I2C via `raspi-config`

Mining Client
=============

Stratum Mining Client:<br>
https://github.com/shufps/piaxe-miner
