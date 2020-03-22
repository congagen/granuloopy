import os
import sys
import wave
import array

from lib import sampler
from lib import mixer

LOOP_COUNT    = 1# if len(sys.argv) < 5 else int(sys.argv[4])
GRAIN_COUNT   = 400# if len(sys.argv) < 6 else int(sys.argv[5])

WND_SIZE_MS   = 800# if len(sys.argv) < 7 else int(sys.argv[6])
STEP_SIZE_MS  = 1# if len(sys.argv) < 8 else int(sys.argv[7])

TEMP_DIR    = "temp"
OUTPUT_DIR  = "output"
OUTPUT_FNA  = sys.argv[1] + "_" + str(LOOP_COUNT) + "_" + str(WND_SIZE_MS) + "_" + str(STEP_SIZE_MS) + ".wav"


def main(input_paths):
    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    abs_path_temp = os.path.abspath(TEMP_DIR)
    abs_path_oput = os.path.abspath(OUTPUT_DIR)

    for i in range(len(input_paths)):

        d_slices = sampler.split_wav_memory_a(
            input_paths[i],
            abs_path_temp,
            loop=LOOP_COUNT,
            window_size_ms=WND_SIZE_MS,
            step_size_ms=STEP_SIZE_MS
        )

        # d_slices = sampler.split_wav_memory(
        #     input_paths[i],
        #     abs_path_temp,
        #     loop=LOOP_COUNT,
        #     grain_count=GRAIN_COUNT
        # )

        mixer.basic_mix_memory_wav(
            d_slices,
            input_paths[i],
            abs_path_oput + "/" + str(i) +"_"+ OUTPUT_FNA
        )


if __name__ == "__main__":
    main([sys.argv[1]])
