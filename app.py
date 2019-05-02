import os
import sys
import wave
import array
import struct

PART_COUNT = 1000
LOOP_COUNT = 6


def slice(infile, frame_rate, start_ms, end_ms):
    fpms   = int(frame_rate / 1000) # frames per ms
    length = int((end_ms - start_ms) * fpms)
    start_index = int(start_ms * fpms)

    infile.rewind()
    anchor = infile.tell()
    infile.setpos(anchor + start_index)

    return infile.readframes(length)


def split_wav(order_path, out_dir="temp/", part_count=1000, loop_count=6):
    w = wave.open(order_path, 'r')

    frame_count = w.getnframes()
    frame_rate  = w.getframerate()
    chan_count  = w.getnchannels()
    comp_type   = w.getcomptype()
    comp_name   = w.getcompname()
    samp_width  = w.getsampwidth()

    window_size_fr = int(frame_count / part_count)
    window_size_ms = int((window_size_fr / frame_rate) * 1000)

    path_list = []

    for p in range(part_count):
        print("Yes: " + str(p))
        for l in range(loop_count):
            start = int(p * window_size_ms)
            stop  = int(start + window_size_ms)

            if start > 0:
                start = start - int(window_size_ms * (1.0 / loop_count))
                stop  = stop  - int(window_size_ms * (1.0 / loop_count))

            sl = slice(w, frame_rate, start, stop)

            out_path = out_dir + "/" + str(p+l) + ".wav"

            sl_out = wave.open(out_path, "w")
            sl_out.setparams((
                chan_count, samp_width, frame_rate,
                window_size_ms, comp_type, comp_name
            ))
            sl_out.writeframes(sl)
            sl_out.close()

            path_list.append(out_path)

    return path_list


def mix_audio(path_list, out_fname="output.wav"):
    with wave.open(out_fname, 'wb') as wav_out:
        for wav_path in path_list:
            with wave.open(wav_path, 'rb') as wav_in:
                if not wav_out.getnframes():
                    wav_out.setparams(wav_in.getparams())
                wav_out.writeframes(wav_in.readframes(wav_in.getnframes()))


w_paths = split_wav(sys.argv[1], part_count=PART_COUNT, loop_count=LOOP_COUNT)
mix_audio(w_paths)
