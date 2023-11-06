
from utils import *

class BmJob:
    def __init__(self):
        self.version = None
        self.prev_block_hash_hex = None
        self.prev_block_hash = None
        self.prev_block_hash_be = None
        self.merkle_root_hex = None
        self.merkle_root = None
        self.merkle_root_be = None
        self.ntime = None
        self.target = None
        self.starting_nonce = 0

        self.num_midstates = 1
        self.difficulty = None

def construct_bm_job(params):
    new_job = BmJob()

    new_job.version = params.version
    new_job.target = params.target
    new_job.ntime = params.ntime
    new_job.difficulty = params.difficulty

    # Convert merkle_root from hex to binary and handle endianness

    new_job.merkle_root = hex2bin(params.merkle_root, 32)
    new_job.merkle_root_be = swap_endian_words(params.merkle_root)
    new_job.merkle_root_be = reverse_bytes(new_job.merkle_root_be)

    # Process previous block hash
    new_job.prev_block_hash = swap_endian_words(params.prev_block_hash)
    new_job.prev_block_hash_be = hex2bin(params.prev_block_hash, 32)
    new_job.prev_block_hash_be = reverse_bytes(new_job.prev_block_hash_be)

    return new_job
