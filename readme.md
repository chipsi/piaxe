Original Repository: https://github.com/skot/bitaxe


This is a variant (Bitaxe ultra 1.3 with BM1366) for Raspberry Pi.

Please don't use it for production yet, the previous version had some issues and the 1.2 version is not yet tested.

![image](https://github.com/shufps/piaxe/assets/3079832/26420be6-9c2b-4226-b3f1-904a380de3df)



Differences:

- powered by 12V and
- added some protection like TVS diode and fuses
- revised buck switching regulator circuit
- revised heatsink
- removed every additional features like DAC, current- and temperature measurement, temperature controlled fan PWM controller, additional testpoints
- replaced level shifter IC with smaller one-channel SC70-5 types
- smallest components have 0805 size for easier manual assembly

Installation:

- add to `/boot/config.txt`:
```
dtoverlay=pwm
```
