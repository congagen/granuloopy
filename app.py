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
    SONG_DUR      = spec["song_duration"]
    OUTPUT_BASE_FILENAME = ""

    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)


    for i in range(len(INPUT_PATHS)):
        rendered_layers = []

        prj_root_dir = OUTPUT_DIR + "/" + str(int(time.time()))

        if not os.path.isdir(prj_root_dir):
            os.mkdir(prj_root_dir)

        prj_dir = prj_root_dir + "/" + str(i+1)

        if not os.path.isdir(prj_dir):
            os.mkdir(prj_dir)

        abs_path_oput = os.path.abspath(prj_dir)

        for layer in spec["layers"].keys():
            layer_spec = spec["layers"][layer]

            sample_offset = layer_spec["sample_offset_ms"]
            sample_size   = layer_spec["sample_size_ms"]
            loop_count    = layer_spec["loop_count"]
            wnd_size_ms   = layer_spec["window_size_ms"]
            step_size_ms  = layer_spec["step_size_ms"]

            output_filename = "LOOP" + str(loop_count) + "_WIN" + str(wnd_size_ms) + "_SMS" + str(step_size_ms)

            layer_data = sampler.split_wav_memory(
                INPUT_PATHS[i],
                song_l=SONG_DUR,
                sample_off=sample_offset,
                sample_size=sample_size,
                loop=loop_count,
                window_size_ms=wnd_size_ms,
                step_size_ms=step_size_ms
            )

            layer_path = abs_path_oput + "/LAYER" + str(layer) + "_" + output_filename + ".wav"

            mixer.mix_slice_list(
                layer_data,
                template_wav=INPUT_PATHS[i],
                out_path=layer_path
            )

            rendered_layers.append(layer_path)

        lcomp_o_path = abs_path_oput + "/" + "MIX.wav"

        if spec["mix_layers"]:
            composite = mixer.mix_layers(
                rendered_layers,
                lcomp_o_path
            )


if __name__ == "__main__":
    main(sys.argv[1])
