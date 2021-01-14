import os
import sys
import json
import time

from lib import sampler
from lib import mixer

TEMP_DIR = "temp"


def main(spec):
    OUTPUT_DIR    = spec["output_dir"]
    SONG_DUR      = spec["song_duration"]
    OUTPUT_BASE_FILENAME = ""

    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    rendered_layers = []
    prj_root_dir = OUTPUT_DIR + "/" + spec["project_name"]

    if not os.path.isdir(prj_root_dir):
        os.mkdir(prj_root_dir)

    prj_dir = prj_root_dir + "/" + str(int(time.time()))

    if not os.path.isdir(prj_dir):
        os.mkdir(prj_dir)

    abs_path_oput = os.path.abspath(prj_dir)

    for layer in spec["layers"].keys():
        print(layer)
        layer_spec = spec["layers"][layer]
        INPUT_PATH = layer_spec["input_path"]

        output_filename = "LOOP" + str(layer_spec["loop_count"]) + "_W" + str(layer_spec["window_size_ms"]) + "_-_" + str(layer_spec["step_size_ms"]) + "MS"

        layer_data = sampler.split_wav_memory(
            layer_spec["input_path"],
            song_l=int(SONG_DUR),
            sample_offset=int(layer_spec["sample_offset_ms"]),
            sample_size=int(layer_spec["sample_size_ms"]),
            loop=int(layer_spec["loop_count"]),
            window_size_ms=int(layer_spec["window_size_ms"]),
            step_size_ms=int(layer_spec["step_size_ms"])
        )

        layer_path = abs_path_oput + "/LAYER" + str(layer) + "_" + output_filename + ".wav"

        mixer.mix_slice_list(
            layer_data,
            template_wav=INPUT_PATH,
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
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as data:
            spec = json.load(data)

        if "prep" in spec.keys():
            orders = sampler.prep_input(spec)

            for o in orders:
                main(o)
        else:
            main(spec)

    else:
        print("Spec path?!")