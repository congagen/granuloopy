import os
import sys
import wave
import array
import struct


def slice(infile, frame_rate, start_ms, end_ms):
    fpms   = int(frame_rate / 1000) # frames per ms
    length = int((end_ms - start_ms) * fpms)
    start_index = int(start_ms * fpms)

    infile.rewind()
    anchor = infile.tell()
    infile.setpos(anchor + start_index)

    return infile.readframes(length)


def mix_file(order_path, out_dir="temp/", part_count = 100, write_slice = True):
    w = wave.open(order_path, 'r')
    composite_audio = array.array('h')

    frame_count = w.getnframes()
    frame_rate  = w.getframerate()
    chan_count  = w.getnchannels()
    comp_type   = w.getcomptype()
    comp_name   = w.getcompname()
    samp_width  = w.getsampwidth()

    window_size_fr = int(frame_count / part_count)
    window_size_ms = int(window_size_fr / frame_rate) * 1000

    for p in range(part_count):
        start = int(p * window_size_ms)
        stop  = int(start + window_size_ms)
        sl     = slice(w, frame_rate, start, stop)

        for i in range(len(sl)):
            composite_audio.append( sl[i] )

        if write_slice:
            out = wave.open(out_dir + "/" + str(p) + ".wav", "w")
            out.setparams(( chan_count, samp_width, frame_rate, window_size_ms, comp_type, comp_name ))
            out.writeframes(sl)

    out = wave.open("output.wav", "w")

    out.setparams((
        chan_count, samp_width, frame_rate,
        window_size_ms, comp_type, comp_name
    ))

    out.writeframes(composite_audio)


def main(order_path):
    mix_file(order_path)


main(sys.argv[1])
