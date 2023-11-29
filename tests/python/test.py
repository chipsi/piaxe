import logging
from crc_package import crc_functions as crc

from bm1366 import bm1366

logging.basicConfig(level=logging.DEBUG)


buffer = bytearray(255)

for i in range(0, 255):
    buffer[i] = i

crc5 = crc.crc5(buffer[:30])
crc16 = crc.crc16(buffer)
crc16_false = crc.crc16_false(buffer)

print(f"crc5 {crc5:02x}")
print(f"crc16 {crc16:04x}")
print(f"crc16_false {crc16_false:04x}")

def tx(data, debug=False):
    print(f"-> {data.hex()}")

def rx(data, timeout, debug=False):
    pass

def reset():
    pass

bm1366.ll_init(tx, rx, reset)


for freq in range(200, 800, 20):
    buf = bm1366.send_hash_frequency(freq)


bm1366.set_job_difficulty_mask(0x00200000)
