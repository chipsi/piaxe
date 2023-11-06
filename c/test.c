#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#include "bm1366.h"

#include "crc.h"

#include "crc.c"
#include "bm1366.c"
#include "utils.c"

int main() {
    uint8_t *buffer = malloc(255);
    for (int i=0;i<255;i++) {
        buffer[i] = i;
    }
    printf("crc5: %02x\n", crc5(buffer, 30));
    printf("crc16: %04x\n", crc16(buffer, 255));
    printf("crc16_false: %04x\n", crc16_false(buffer, 255));

    for (int freq=200; freq<800; freq+=20) {
        BM1366_send_hash_frequency(freq);
    }

    BM1366_set_job_difficulty_mask(0x00200000);


    const char* job="1801000000feffff7f20545ad924aab31471bc9b048a10decd1270dda2085f04ede2ca938569ee9493869d10aa520000000000000000eb48ca0c910d334bd346d9e82a30ca441680a286b6ff0b1b00000002";
    uint8_t* job_bytes = malloc(strlen(job) / 2);
    hex2bin(job, job_bytes, strlen(job)/2);

    _send_BM1366((TYPE_JOB | GROUP_SINGLE | CMD_WRITE), job_bytes, strlen(job)/2, true);

    const char* merkle_root = "9d10aa52ee949386ca9385695f04ede270dda20810decd12bc9b048aaab31471";
    char bin_buffer[32];
    char bin_buffer_be[32];

    hex2bin(merkle_root, bin_buffer, sizeof(bin_buffer));
    printf("%s\n", merkle_root);
    for (int i=0;i<sizeof(bin_buffer);i++) {
        printf("%02x", bin_buffer[i]);
    }
    printf("\n\n");

    // hex2bin(merkle_root, new_job.merkle_root_be, 32);
    swap_endian_words(merkle_root, bin_buffer_be);
    reverse_bytes(bin_buffer_be, 32);

    printf("%s\n", merkle_root);
    for (int i=0;i<sizeof(bin_buffer_be);i++) {
        printf("%02x", bin_buffer_be[i]);
    }
    printf("\n\n");


    return 0;
}