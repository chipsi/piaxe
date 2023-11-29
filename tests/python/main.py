import RPi.GPIO as GPIO
import serial
import time
import math
import logging
import struct
import hashlib

from rpi_hardware_pwm import HardwarePWM

from crc_package.crc_functions import crc5, crc16_false
from bm1366 import bm1366, utils

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
bm1366.init(485)
init_response = bm1366.receive_work()

if init_response.nonce != 0x00006613:
    raise Exception("bm1366 not detected")

#bm1366.set_job_difficulty_mask(64)

def reverse_hex(hex_string):
    bytes = utils.hex2bin(hex_string)
    return bytearray(bytes[::-1]).hex()


work = bm1366.WorkRequest()


merkle_root_be = utils.swap_endianness_32bit(utils.hex2bin("768c54aa39f020353f6474b7b14e0add32e29cbd67b44326eb869f4557ce2f3d"))
prev_block_hash_be = utils.swap_endianness_32bit(utils.hex2bin("00000000000000000000332ccd3fb7c76ee315ba66b731bee66d49c8458bc095"))

work.create_work(
    0x28,
    0x00000000,
    0x187fffff, #nbits
    0x654de8ae,
    merkle_root_be,
    prev_block_hash_be,
    0x20000000
)
bm1366.send_work(work)

work.merkle_root = utils.hex2bin(reverse_hex("768c54aa39f020353f6474b7b14e0add32e29cbd67b44326eb869f4557ce2f3d"))
work.prev_block_hash = utils.hex2bin(reverse_hex("00000000000000000000332ccd3fb7c76ee315ba66b731bee66d49c8458bc095"))

time.sleep(0.5)


#cgminer nonce testing
# truediffone == 0x00000000FFFF0000000000000000000000000000000000000000000000000000
truediffone = 26959535291011309493156476344723991336010898738574164086137773096960.0


def verify_work(work, result):
    work.print()
    result.print()
    header = struct.pack('<I', work.version | (bm1366.reverse_uint16(result.version) << 13))
    header += work.prev_block_hash
    header += work.merkle_root
    header += struct.pack('<I', work.ntime)
    header += struct.pack('<I', work.nbits)
    header += struct.pack('<I', result.nonce)
    logging.debug("header: %s", bytearray(header).hex())

    # Hash the header twice using SHA-256.
    hash_buffer = hashlib.sha256(header).digest()
    hash_result = hashlib.sha256(hash_buffer).digest()
    logging.debug("result: %s", bytearray(hash_result).hex())
    #d64 = truediffone
    #s64 = utils.le256todouble(hash_result)
    #ds = d64 / s64
    return hash_result #ds

if False:
    dummywork = bm1366.WorkRequest()
    dummywork.version = 838860800
    dummywork.prev_block_hash = utils.hex2bin(reverse_hex("00000000000000000000332ccd3fb7c76ee315ba66b731bee66d49c8458bc095"))
    dummywork.merkle_root = utils.hex2bin(reverse_hex("768c54aa39f020353f6474b7b14e0add32e29cbd67b44326eb869f4557ce2f3d"))
    dummywork.ntime = 1699604654
    dummywork.nbits = 386171284


    dummyresult = bm1366.AsicResult()
    dummyresult.nonce = 3420097076
    dummyresult.version = 0

    verify_work(dummywork, dummyresult)

while True:
    result = bm1366.receive_work()
    # we assume we have some work done
    if result and result.nonce and result.nonce not in [0x0, 0x6613]:
        verify_work(work, result)


serial_port.close()  # Close the serial port

#pwm.stop()

# shutdown power supply
GPIO.output(SDN_PIN, True)

GPIO.cleanup()  # Reset the state of the GPIO pins
