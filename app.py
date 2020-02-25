import os
import sys
import wave
import array

from lib import sampler
from lib import mixer


SLICE_COUNT = 200 if len(sys.argv) < 3 else int(sys.argv[2])
LOOP_COUNT  = 16  if len(sys.argv) < 4 else int(sys.argv[3])
GRAIN_COUNT = 4   if len(sys.argv) < 5 else int(sys.argv[4])
LAYERS      = 1

TEMP_DIR    = "temp"
OUTPUT_DIR  = "output"
OUTPUT_FNA  = str(SLICE_COUNT) + "_" + str(LOOP_COUNT) + "_" + str(GRAIN_COUNT) + ".wav"


def main(input_paths):
    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    abs_path_temp = os.path.abspath(TEMP_DIR)
    abs_path_oput = os.path.abspath(OUTPUT_DIR)

    for i in range(len(input_paths)):

        d_slices = sampler.split_wav_memory(
            input_paths[i], abs_path_temp,
            part_count  = SLICE_COUNT,
            loop_count  = LOOP_COUNT,
            grain_count = GRAIN_COUNT
        )

        mixer.basic_mix_memory(
            d_slices,
            input_paths[0],
            abs_path_oput + "/" + str(i) +"_"+ OUTPUT_FNA
        )


if __name__ == "__main__":
    main([sys.argv[1]])
