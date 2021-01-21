import wave
import random
import os
import copy
import time
from lib import mixer


def cut_segment(infile, fpms, length, start_ms, end_ms):
    length = int((end_ms - start_ms) * fpms)
    start_index = int(start_ms * fpms)

    infile.rewind()
    anchor = infile.tell()
    infile.setpos(anchor + start_index)

    return infile.readframes(length)


def conform_length(track_frames, track_length, frame_rate=44100):
    fr = []
    target_frame_count = int(frame_rate * (track_length * 60))

    if len(track_frames) < target_frame_count:
        while len(fr) < target_frame_count:
            for f in track_frames:
                fr.append(f)
    else:
        fr = track_frames[:target_frame_count]

    return fr


def split_wav_memory(input_file_path, song_l=0, sample_offset=0, sample_size=20000, loop=1, window_size_ms=200, step_size_ms=50):
    w = wave.open(input_file_path, 'r')
    data_slices = []

    input_frame_count = w.getnframes()
    input_frame_rate  = w.getframerate()
    input_file_len_ms = int((input_frame_count / input_frame_rate) * 1000)
    input_sample_size = sample_size if sample_size != 0 else input_file_len_ms

    output_song_len_ms = int((song_l * 60) * 1000)

    if int(input_file_len_ms) < input_sample_size:
        print("file_len_ms > input_sample_size")
        input_sample_size = input_file_len_ms

    if window_size_ms > input_sample_size:
        print("file_len_ms > input_sample_size")
        window_size_ms = input_sample_size

    frames_per_ms  = int(input_frame_rate / 1000)
    step_count     = int((input_file_len_ms - sample_offset) / int(window_size_ms+step_size_ms))

    cur_len_ms = 0
    loop = 1 if loop == 0 else loop

    while cur_len_ms < output_song_len_ms:
        print("Splitting: " + str(cur_len_ms) + "/" + str(output_song_len_ms))
        for s in range(step_count):
            print("Step: " + str(s) + " / " + str(step_count))

            start = sample_offset + int(step_size_ms * s)
            stop = int(start + window_size_ms)
            #print("Stop " + str(stop) + " - File Len: " + str(file_len_ms))

            if stop < input_file_len_ms:
                for i_l in range(loop):
                    length = int((stop - start) * frames_per_ms)
                    seg = cut_segment(w, frames_per_ms, length, start, stop)
                    if cur_len_ms < output_song_len_ms:
                        data_slices.append(seg)
                    cur_len_ms += window_size_ms
            else:
                print("ERROR")
                return

    return data_slices


def cut_samples(input_file_path, sample_size_ms=2000, step_ratio=1):
    w = wave.open(input_file_path, 'r')
    data_slices = []

    step_size_ms = int(sample_size_ms * step_ratio)

    frame_count = w.getnframes()
    frame_rate  = w.getframerate()
    chan_count  = w.getnchannels()

    file_len_ms = int((frame_count / frame_rate) * 1000)

    part_count     = file_len_ms / sample_size_ms
    frames_per_ms  = int(frame_rate / 1000)
    step_count     = int(file_len_ms / step_size_ms)

    cur_len_ms = 0

    for s in range(step_count):
        start = int(step_size_ms * s)
        stop = int(start + sample_size_ms)

        if stop < file_len_ms:
            length = int((stop - start) * frames_per_ms)
            seg = cut_segment(w, frames_per_ms, length, start, stop)
            if cur_len_ms < file_len_ms:
                data_slices.append(seg)
            cur_len_ms += sample_size_ms

    return data_slices


def prep_input(spec):
    slices = []
    orders = []

    for k in spec["prep"].keys():
        t_dir = spec["project_name"] + "_" + str(int(time.time()))

        temp_dir = spec["prep"][k]["prep_dir"]
        if not os.path.isdir(temp_dir):
            os.mkdir(temp_dir)

        if not os.path.isdir(temp_dir + "/" + t_dir):
            os.mkdir(temp_dir + "/" + t_dir)

        o_dir = (temp_dir + "/" + t_dir + "/" + str(k))
        if not os.path.isdir(o_dir):
            os.mkdir(o_dir)

        itm = spec["prep"][k]

        data_slice_list = cut_samples(
            itm["input_path"], itm["sample_size_ms"], itm["step_ratio"]
        )
        c = 0

        for s in range(len(data_slice_list)):
            op = o_dir + "/" + str(k) +"_"+ str(c) + ".wav"
            c += 1
            slices.append(op)

            mixer.write_audio_bytes(op, data_slice_list[s])
            l_spec = copy.deepcopy(spec)

            for l in l_spec["layers"].keys():
                l_spec["layers"][l]["input_path"] = op

            orders.append(l_spec)

        if spec["randomize_layers"]:
            for o in range(len(orders)):
                for l in orders[o]["layers"].keys():
                    orders[o]["layers"][l]["input_path"] = random.choice(slices)

    return orders
