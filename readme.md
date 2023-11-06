Original Repository: https://github.com/skot/bitaxe


This is an **untested** variant (Bitaxe ultra 1.2 with BM1366) for Raspberry Pi.

![image](https://github.com/shufps/piaxe/assets/3079832/b90d2969-18e5-4343-8539-26ef8817bfae)




Differences:

- powered by 12V and
- added some protection like TVS diode and fuses
- revised buck switching regulator circuit
- revised heatsink
- removed every additional features like DAC, current- and temperature measurement, temperature controlled fan PWM controller, additional testpoints
- replaced level shifter IC with cheaper mosfets
- smallest components have 0805 size for easier manual assembly

Installation:

- add to `/boot/config.txt`:
```
dtoverlay=pwm
```
