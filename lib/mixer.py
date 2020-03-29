import random
import wave
import array
import math
import numpy as np


def write_audio(file_path, audio_data, frame_count=0, num_chan=2, s_rate=44100):
    n_chan = max(min(num_chan, 1), 2)
    frame_count = len(audio_data) if frame_count == 0 else frame_count

    f = wave.open(file_path, 'w')
    f.setparams((n_chan, 2, s_rate, frame_count, "NONE", "Uncompressed"))
    f.writeframes(audio_data.tobytes())
    f.close()


def mix_slice_list(data_list, template_wav, out_path="output.wav"):
    with wave.open(template_wav, 'rb') as template:
        with wave.open(out_path, 'wb') as wav_out:
            for i in range(len(data_list)):
                data_slice = data_list[i]
                print("Writing: " + str(i) + " / " + str(len(data_list)))
                if not wav_out.getnframes():
                    wav_out.setparams(template.getparams())
                wav_out.writeframes(data_slice)


def mix_layers(input_paths, o_path, max_amplitude=30000):
    print("Mixing layers...")
    mixed_audio_data = array.array('h')
    layer_frames = []
    mix = []

    print(o_path)
    w = wave.open(input_paths[0], 'rb')
    frame_count    = w.getnframes()
    frame_rate     = w.getframerate()
    chan_count     = w.getnchannels()
    comp_type      = w.getcomptype()
    comp_name      = w.getcompname()
    samp_width     = w.getsampwidth()
    w_frames       = w.readframes(frame_count)

    waves = [wave.open(fn) for fn in input_paths]
    frames = [w.readframes(w.getnframes()) for w in waves]

    layer_count = len(frames)

    samples = [np.frombuffer(f, dtype='<i2') for f in frames]
    samples = [samp.astype(np.float64) for samp in samples]
    n = min(map(len, samples))

    mix = samples[0][:n]
    mix = np.true_divide(mix, layer_count)

    for s in range(1, len(samples)):
        m = samples[s][:n]
        m = np.true_divide(m, layer_count)
        mix += m
        #mix += [(s / layer_count) for s in samples[s][:n]]

    mix_wav = wave.open(o_path, 'w')
    mix_wav.setparams(w.getparams())
    mix_wav.writeframes(mix.astype('<i2').tobytes())
    mix_wav.close()
