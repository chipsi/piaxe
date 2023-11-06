import RPi.GPIO as GPIO
import serial
import time
import math
import logging

from rpi_hardware_pwm import HardwarePWM

from crc_package.crc_functions import crc5, crc16_false
from bm1366 import bm1366

from stratum import utils

logging.basicConfig(level=logging.DEBUG)

# Setup GPIO
GPIO.setmode(GPIO.BOARD)  # Use Physical pin numbering

# Define the pin numbers:
SDN_PIN = 11  # SDN, output, initial high
PGOOD_PIN = 13  # PGOOD, input, floating
NRST_PIN = 15  # NRST, output, initial high
PWM_PIN = 12  # PWM output on Pin 12

# Initialize GPIO Pins
GPIO.setup(SDN_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PGOOD_PIN, GPIO.IN)  # Default is floating
GPIO.setup(NRST_PIN, GPIO.OUT, initial=GPIO.HIGH)

pwm = HardwarePWM(pwm_channel=0, hz=1000)
pwm.start(80) # full duty cycle

# Initialize serial communication
serial_port = serial.Serial(
    port="/dev/ttyS0",  # For GPIO serial communication use /dev/ttyS0
    baudrate=115200,    # Set baud rate to 115200
    bytesize=serial.EIGHTBITS,    # Number of data bits
    parity=serial.PARITY_NONE,    # No parity
    stopbits=serial.STOPBITS_ONE, # Number of stop bits
    timeout=1                     # Set a read timeout
)

def serial_tx_func(data, debug=False):
    serial_port.write(data)
    logging.debug("-> %s", bytearray(data).hex())
    time.sleep(0.01)

def serial_rx_func(size, timeout_ms, debug=False):
    serial_port.timeout = timeout_ms / 1000.0

    data = serial_port.read(size)
    bytes_read = len(data)

    logging.debug("serial_rx: %d", bytes_read)
    if bytes_read > 0:
        logging.debug("<- %s", data.hex())

    return data

def reset_func():
    GPIO.output(NRST_PIN, True)
    time.sleep(0.5)
    GPIO.output(NRST_PIN, False)
    time.sleep(0.5)

def is_power_good():
    return GPIO.input(PGOOD_PIN)


GPIO.output(SDN_PIN, False)


while (not is_power_good()):
    print("power not good ... waiting ...")
    time.sleep(5)


# set the hardware dependent functions for serial and reset
bm1366.ll_init(serial_tx_func, serial_rx_func, reset_func)

# init bm1366
bm1366.init(200)
init_response = bm1366.receive_work()

if init_response.nonce != 0x00006613:
    raise Exception("bm1366 not detected")


bm1366.set_job_difficulty_mask(64)

if False:
    for i in range(0, 5):
        print(f"send {i}")
        bm1366.send_work(
            (i + 8) % 128,
            0x8826bf10,
            0x17048194, #0x30c31b18, #nbits
            0x647384a0,
            utils.hex_to_be("1bbac7eab8feaab5a75a1f1fd8f15fedb008d4ca8270262eedd62f17e672da03"),
            utils.hex_to_be("0000000000000000000005674e8b6be06d49a4de2691660b1393feb9e6ece8d8"),
            0x20000000
        )
        time.sleep(0.5)

hex_string = "55AA216100100000000F8952419E016AF64E447CC41EED1CB9CD5511694CB4D9BA0DDA5A1EF88450BA68D96216ECF5630BC000000000C000000659049105857DDA2478A5E7CCCFE036FE8BE8EF8C25721D400000020ECBE"

if True:
	bm1366.send_work(
	    0x28,
	    0x00000000,
	    0x207fffff, #nbits
	    0x64af16e0,
	    bytearray.fromhex("F3C00910CBDAF23F0FFFDF3F7B42ACC98D70ED9BBFBA1B1D4474EDE0322885C7"),
	    bytearray.fromhex("000000000C000000659049105857DDA2478A5E7CCCFE036FE8BE8EF8C25721D4"),
	    0x20000000
	)
time.sleep(0.5)


# Remove spaces and convert to a bytearray
#byte_array = bytearray.fromhex(hex_string)

#bm1366.send_simple(byte_array)

#try:

while False:
    serial_port.timeout = 60.0

    data = serial_port.read(1)
    print(f"{data[0]:02x}")


#bm1366.send_simple([0x55, 0xAA, 0x52, 0x05, 0x00, 0x00, 0x0A])

result = bm1366.receive_work()
print(str(result))
#except Exception as e:
#    print(e)


#print("waiting 30...")
#time.sleep(30)

serial_port.close()  # Close the serial port

#pwm.stop()

# shutdown power supply
GPIO.output(SDN_PIN, True)


GPIO.cleanup()  # Reset the state of the GPIO pins
