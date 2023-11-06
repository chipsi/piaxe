import time
from rpi_hardware_pwm import HardwarePWM

pwm = HardwarePWM(pwm_channel=0, hz=1000)
pwm.start(50) # full duty cycle

pwm.change_duty_cycle(50)
pwm.change_frequency(1_000)

time.sleep(30)

pwm.stop()

