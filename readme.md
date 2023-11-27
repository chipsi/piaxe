Original Repository: https://github.com/skot/bitaxe


This is a variant (Bitaxe ultra 1.3 with BM1366) for Raspberry Pi.

Update: Miner is running stable 🥳


![image](https://github.com/shufps/piaxe/assets/3079832/1b79eda2-acb0-4a86-ad00-c1af6b7e4b8b)




Differences:

- powered by 12V and
- added some protection like TVS diode and fuses
- revised buck switching regulator circuit
- revised heatsink
- removed every additional features like DAC, current- and temperature measurement, temperature controlled fan PWM controller, additional testpoints
- replaced level shifter IC with smaller one-channel SC70-5 types
- smallest components have 0805 size for easier manual assembly
- LM75 compatible temperature sensor under the heatsink

Installation:

- add to `/boot/config.txt`:
```
dtoverlay=pwm
```
