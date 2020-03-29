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


def split_wav_memory(input_file_path, song_l=0, sample_off=0, sample_size=20000, loop=1, window_size_ms=200, step_size_ms=50):
    w = wave.open(input_file_path, 'r')
    data_slices = []

    frame_count    = w.getnframes()
    frame_rate     = w.getframerate()
    chan_count     = w.getnchannels()

    song_len_ms = int((song_l * 60) * 1000)
    file_len_ms = int((frame_count / frame_rate) * 1000) - sample_off

    if file_len_ms > sample_size:
        file_len_ms = sample_size

    if file_len_ms > song_len_ms:
        file_len_ms = song_len_ms

    part_count     = file_len_ms / window_size_ms
    frames_per_ms  = int(frame_rate / 1000)
    step_count     = int(file_len_ms / step_size_ms)

    cur_len_ms = 0

    while cur_len_ms < song_len_ms:
        for s in range(step_count):
            start = sample_off + int(step_size_ms * s)
            stop = int(start + window_size_ms)

            if stop < file_len_ms:
                for i_l in range(loop):
                    print("Splitting... ")

                    length = int((stop - start) * frames_per_ms)
                    seg = cut_segment(w, frames_per_ms, length, start, stop)
                    if cur_len_ms < song_len_ms:
                        data_slices.append(seg)
                    cur_len_ms += window_size_ms

    return data_slices
