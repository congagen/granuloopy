import os
import sys
import wave
import array

from lib import sampler
from lib import mixer

PART_COUNT  = 200 if len(sys.argv) < 3 else int(sys.argv[2])
LOOP_COUNT  = 16  if len(sys.argv) < 4 else int(sys.argv[3])
GRAIN_COUNT = 2   if len(sys.argv) < 4 else int(sys.argv[3])
LAYERS      = 3

TEMP_DIR    = "temp"
OUTPUT_DIR  = "output"
OUTPUT_FNA  = str(PART_COUNT) + "_" + str(LOOP_COUNT) + "_" + str(GRAIN_COUNT) + ".wav"


def main(input_paths):
    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    abs_path_temp = os.path.abspath(TEMP_DIR)
    abs_path_oput = os.path.abspath(OUTPUT_DIR)

    for p in input_paths:

        w_paths = sampler.split_wav(
            p, abs_path_temp,
            part_count=PART_COUNT,
            loop_count=LOOP_COUNT,
            grain_count=GRAIN_COUNT
        )

        mixer.basic_mix(w_paths, abs_path_oput + "/" + OUTPUT_FNA)


if __name__ == "__main__":
    main([sys.argv[1]])
