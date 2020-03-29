import os
import sys
import json
import time

from lib import sampler
from lib import mixer


TEMP_DIR = "temp"


def main(spec_path):
    with open(spec_path) as data:
        spec = json.load(data)

    INPUT_PATHS   = spec["input_paths"]
    OUTPUT_DIR    = spec["output_dir"]
    PRJ_DIR = OUTPUT_DIR+"/"+str(time.time())

    LAYER_COUNT   = len(spec["layers"].keys())
    SONG_DUR      = spec["song_duration"]

    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    if not os.path.isdir(PRJ_DIR):
        os.mkdir(PRJ_DIR)

    abs_path_oput = os.path.abspath(PRJ_DIR)

    for i in range(len(INPUT_PATHS)):
        rendered_layers = []

        for layer in spec["layers"].keys():
            layer_spec = spec["layers"][layer]

            SAMPLE_OFFSET = layer_spec["sample_offset_ms"]
            SAMPLE_SIZE   = layer_spec["sample_size_ms"]
            LOOP_COUNT    = layer_spec["loop_count"]
            WND_SIZE_MS   = layer_spec["window_size_ms"]
            STEP_SIZE_MS  = layer_spec["step_size_ms"]

            OUTPUT_FNA = str() + INPUT_PATHS[i] + "_W" + str(WND_SIZE_MS) + "_LO" + str(LOOP_COUNT) + "_S" + str(STEP_SIZE_MS)

            audio_data = sampler.split_wav_memory(
                INPUT_PATHS[i],
                song_l=SONG_DUR,
                sample_off=SAMPLE_OFFSET,
                sample_size=SAMPLE_SIZE,
                loop=LOOP_COUNT,
                window_size_ms=WND_SIZE_MS,
                step_size_ms=STEP_SIZE_MS
            )

            comp_opath_a = abs_path_oput + "/" + str(i) + "_" + OUTPUT_FNA + "_LAYER" + str(layer) + ".wav"

            mixer.mix_slice_list(
                audio_data,
                INPUT_PATHS[i],
                comp_opath_a
            )

            rendered_layers.append(comp_opath_a)

        lcomp_o_path = abs_path_oput + "/" + str(i) + "_" + OUTPUT_FNA + "_COMP" + str(LAYER_COUNT) + ".wav"

        if spec["mix_layers"]:
            composite = mixer.mix_layers(
                rendered_layers,
                SONG_DUR,
                lcomp_o_path
            )


if __name__ == "__main__":
    main(sys.argv[1])
