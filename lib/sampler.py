import wave


def cut_segment(infile, fpms, length, start_ms, end_ms):
    length = int((end_ms - start_ms) * fpms)
    start_index = int(start_ms * fpms)

    infile.rewind()
    anchor = infile.tell()
    infile.setpos(anchor + start_index)

    return infile.readframes(length)


def split_wav(input_file_path, out_dir="temp/", part_count=1000, loop_count=6):
    w = wave.open(input_file_path, 'r')

    frame_count   = w.getnframes()
    frame_rate    = w.getframerate()
    chan_count    = w.getnchannels()
    comp_type     = w.getcomptype()
    comp_name     = w.getcompname()
    samp_width    = w.getsampwidth()

    window_size_fr = int(frame_count / part_count)
    window_size_ms = int((window_size_fr / frame_rate) * 1000)
    fr_per_sec     = int(frame_rate / 1000)

    path_list = []

    for p in range(part_count):
        print(str(p) + " / " + str(part_count))

        for l in range(loop_count):

            start = int(p * window_size_ms)
            stop  = int(start + window_size_ms)

            if start > 0:
                start = start - int(window_size_ms * (1.0 / loop_count))
                stop  = stop  - int(window_size_ms * (1.0 / loop_count))

            length = int((stop - start) * fr_per_sec)

            sl = cut_segment(w, fr_per_sec, length, start, stop)

            out_path = out_dir + "/" + str(p) + "_" + str(l) + ".wav"

            sl_out = wave.open(out_path, "w")
            sl_out.setparams((
                chan_count, samp_width, frame_rate,
                window_size_ms, comp_type, comp_name
            ))

            sl_out.writeframes(sl)
            sl_out.close()

            path_list.append(out_path)

    return path_list
