import random
import wave


def basic_mix_files(path_list, out_path="output.wav"):
    with wave.open(out_path, 'wb') as wav_out:
        for wav_path in path_list:
            print("Mixing: " + str(wav_path))
            with wave.open(wav_path, 'rb') as wav_in:
                if not wav_out.getnframes():
                    wav_out.setparams(wav_in.getparams())
                wav_out.writeframes(wav_in.readframes(wav_in.getnframes()))


def basic_mix_memory(data_list, template_wav, out_path="output.wav"):
    with wave.open(template_wav, 'rb') as template:

        with wave.open(out_path, 'wb') as wav_out:
            for data_slice in data_list:
                if not wav_out.getnframes():
                    wav_out.setparams(template.getparams())
                wav_out.writeframes(data_slice)


def mix_random(path_list, length=0, out_path="output.wav"):
    with wave.open(out_path, 'wb') as wav_out:

        if length == 0:
            length = len(path_list)

        for i in range(length):

            r_path = random.choice(path_list)

            print("Mixing: " + str(wav_path))
            with wave.open(r_path, 'rb') as wav_in:
                if not wav_out.getnframes():
                    wav_out.setparams(wav_in.getparams())
                wav_out.writeframes(wav_in.readframes(wav_in.getnframes()))
