import random
import wave
import aifc


def basic_mix_wav_files(path_list, out_path="output.wav"):
    with wave.open(out_path, 'wb') as wav_out:
        for wav_path in path_list:
            print("Mixing: " + str(wav_path))
            with wave.open(wav_path, 'rb') as wav_in:
                if not wav_out.getnframes():
                    wav_out.setparams(wav_in.getparams())
                wav_out.writeframes(wav_in.readframes(wav_in.getnframes()))


def basic_mix_memory_wav(data_list, template_wav, out_path="output.wav"):
    with wave.open(template_wav, 'rb') as template:

        with wave.open(out_path, 'wb') as wav_out:
            for i in range(len(data_list)):
                print("Writing: " + str(i) + " / " + str(len(data_list)))
                data_slice = data_list[i]
                if not wav_out.getnframes():
                    wav_out.setparams(template.getparams())
                wav_out.writeframes(data_slice)


def basic_mix_memory_aif(data_list, template_wav, out_path="output.wav"):
    with aifc.open(template_wav, 'rb') as template:
        framerate     = template.getframerate()
        nchannels     = template.getnchannels()
        comptype      = template.getcomptype()
        compname      = template.getcompname()
        sampwidth     = template.getsampwidth()

        with aifc.open(out_path, 'wb') as aif_out:
            for i in range(len(data_list)):
                print("Writing: " + str(i) + " / " + str(len(data_list)))
                data_slice = data_list[i]
                if not aif_out.getnframes():
                    aif_out.setparams(
                        (nchannels, sampwidth, framerate,
                        len(data_list), b'NONE', compname)
                    )
                aif_out.writeframes(data_slice)
                #aif_out.writeframes(str(ord(str(data_slice)[0])).encode())



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
