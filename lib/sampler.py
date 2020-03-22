import wave
import aifc
import random


def cut_segment(infile, fpms, length, start_ms, end_ms):
    length = int((end_ms - start_ms) * fpms)
    start_index = int(start_ms * fpms)

    infile.rewind()
    anchor = infile.tell()
    infile.setpos(anchor + start_index)

    return infile.readframes(length)


def split_wav_memory_a(input_file_path, out_dir="temp/", loop=8, window_size_ms=200, step_size_ms=50):
    w = wave.open(input_file_path, 'r')
    data_slices = []

    frame_count    = w.getnframes()
    frame_rate     = w.getframerate()
    chan_count     = w.getnchannels()
    comp_type      = w.getcomptype()
    comp_name      = w.getcompname()
    samp_width     = w.getsampwidth()

    file_len_ms    = int((frame_count / frame_rate) * 1000)
    part_count     = file_len_ms / window_size_ms
    fr_per_sec     = int(frame_rate / 1000)

    step_count = int(file_len_ms / step_size_ms)

    for s in range(step_count):
        start = int(step_size_ms * s)
        stop = int(start + window_size_ms)

        if stop < file_len_ms:
            for i_l in range(loop):
                print("Splitting... " + random.choice(["I", "O"]) )

                length = int((stop - start) * fr_per_sec)
                sl = cut_segment(w, fr_per_sec, length, start, stop)
                data_slices.append(sl)

    return data_slices



def split_wav_memory_b(input_file_path, out_dir="temp/", loop=8, grain_count=100):
    w = wave.open(input_file_path, 'r')
    data_slices = []

    frame_count    = w.getnframes()
    frame_rate     = w.getframerate()
    chan_count     = w.getnchannels()
    comp_type      = w.getcomptype()
    comp_name      = w.getcompname()
    samp_width     = w.getsampwidth()

    window_size_fr = int(frame_count / grain_count)
    window_size_ms = int((window_size_fr / frame_rate) * 1000)
    file_len_ms    = int((frame_count / frame_rate) * 1000)
    fr_per_sec     = int(frame_rate / 1000)

    path_list = []

#    for p in range(part_count):

    for g in range(grain_count):
        start = int(window_size_ms * g)
        stop = int(start + window_size_ms)
        #g_offset = ((window_size_ms / grain_count) * g)

        for i_l in range(loop):
            print("Splitting... " + random.choice(["I", "O"]) )

            #if start > 0 and int(stop  + g_offset) < file_len_ms:
            #    start = int(start + g_offset)
            #    stop  = int(stop  + g_offset)

            l_offset = ((window_size_ms / loop) * i_l)

            #if start > 0 and int(stop  + l_offset) < file_len_ms:
            #    start = int(start + l_offset)
            #    stop  = int(stop  + l_offset)

            length = int((stop - start) * fr_per_sec)
            sl = cut_segment(w, fr_per_sec, length, start, stop)
            data_slices.append(sl)

    return data_slices


