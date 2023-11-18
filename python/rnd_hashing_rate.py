import RPi.GPIO as GPIO
import serial
import time
import math
import logging
import struct
import hashlib
import random
import threading

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


def random_merkle_root():
    """Generate a random Merkle root in the required format."""
    return ''.join(random.choices('0123456789abcdef', k=64))


def reverse_hex(hex_string):
    bytes = utils.hex2bin(hex_string)
    return bytearray(bytes[::-1]).hex()

def calculate_hash_rate_from_difficulty(difficulty, average_time):
    """Calculate hash rate in GH/s (Gigahashes per second)."""
    num_bits = int(math.log(difficulty) / math.log(2)) + 32

    hash_rate_hps = 2**num_bits / average_time  # Hash rate in H/s
    hash_rate_ghps = hash_rate_hps / 1e9  # Convert to GH/s
    return hash_rate_ghps

def count_leading_zeros(hex_string):
    # Convert the hexadecimal string to a binary string
    binary_string = bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)

    # Count the leading zeros
    count = 0
    for char in binary_string:
        if char == '0':
            count += 1
        else:
            break

    return count

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
    hash_str = bytearray(hash_result).hex()
    hash_be = utils.swap_endianness_32bit(utils.hex_to_be(hash_str))
    hash_str = bytearray(hash_be).hex()
    leading_zeros = count_leading_zeros(hash_str)
    logging.debug("result: %s (%d)", hash_str, leading_zeros)
    #d64 = truediffone
    #s64 = utils.le256todouble(hash_result)
    #ds = d64 / s64
    return leading_zeros #ds


nbits = 0x17048194  # Example nbits value
total_time = 0

# 32 -> 37 zeros
# 64 -> 38 zeros
# 128 -> 39 zeros
# 256 -> 40 zeros
difficulty = 128
bm1366.set_job_difficulty_mask(difficulty)

num_samples = 1000

# 2.5s at 32
# 5s at 64
difficulty_bits = int(math.log(difficulty)/math.log(2))
timeout = 2500*2**(difficulty_bits-5)

print(f"timeout set to: {timeout}ms")

work = bm1366.WorkRequest()
err = None
result_received = dict()

def thread_function(event):
    global err, result_received
    print("receiving thread started ...")
    while True:
        result = bm1366.receive_work(timeout)
        if not result or not result.nonce:
            continue

        if result.nonce == 0x6613 and result.job_id == 0:
            # not interested in chip id response
            continue

        #if result.job_id & 0xf8 != work.id:
        #    print(f"ignoring result for job {result.job_id:02x}")
        #    continue

        print(f"received job {result.job_id:02x}")
        lock.acquire()
        result_received[result.job_id & 0xf8] = result
        event.set()
        lock.release()


event = threading.Event()
lock = threading.Lock()

threading.Thread(target=thread_function, args=(event,)).start()

timeouts = 0
bad_results = 0
# Loop for 1000 iterations
for i in range(1, num_samples):
    merkle_root_hex = random_merkle_root()
    merkle_root_be = utils.swap_endianness_32bit(utils.hex2bin(merkle_root_hex))
    prev_block_hash_be = utils.swap_endianness_32bit(utils.hex2bin("0000000000000000000009eca4c4b04aed3aae572b820369c7d153c08bfa986d"))

    job_id = (i << 3) & 0xff
    work.create_work(
        job_id,
        0x00000000,
        nbits,
        0x654de8ae,
        merkle_root_be,
        prev_block_hash_be,
        0x20000000
    )

    start_time = time.time()
    bm1366.send_work(work)

    work.merkle_root = utils.hex2bin(reverse_hex(merkle_root_hex))
    work.prev_block_hash = utils.hex2bin(reverse_hex("0000000000000000000009eca4c4b04aed3aae572b820369c7d153c08bfa986d"))

    print(f"submitted job {job_id:02x}")

    # wait for job done
    event_set = event.wait(timeout=timeout / 1000.0)
    if not event_set:
        print("timeout ...")
        timeouts += 1
        # timeout
        continue

    lock.acquire()
    event.clear()

    if work.id in result_received and result_received[work.id]:
        result = result_received[work.id]
    # we are not interested in the rest
    result_received = dict()

    lock.release()

    if not result:
        continue

    # verify work
    mwm = verify_work(work, result)
    if mwm < 32 + difficulty_bits:
        print("bad result")
        bad_results += 1
        continue

    elapsed = time.time() - work.time
    print(f"{i} took {elapsed}")
    total_time += time.time() - start_time


    # reset error flag


# Calculate average time and hash rate
average_time = total_time / num_samples
hash_rate = calculate_hash_rate_from_difficulty(difficulty, average_time)

print(f"Average Time: {average_time} seconds")
print(f"Hash Rate: {hash_rate} GH/s")
print(f"Timeouts: {timeouts}")
print(f"Bad Results: {bad_results}")







serial_port.close()  # Close the serial port

#pwm.stop()

# shutdown power supply
GPIO.output(SDN_PIN, True)

GPIO.cleanup()  # Reset the state of the GPIO pins
