from typing import Union, Tuple, Optional

import numpy as np
from numpy import ndarray
from scipy.io.wavfile import write
import sounddevice as sd
import matplotlib.pyplot as plt
import random


def generate_sound():
    sample_rate = 1000
    duration = 1
    frequencies = [440, 554, 0, 660, 280, 800, 440, 660, 554, 440, 0, 300, 350, 400, 450, 500, 450, 400, 350, 300]

    t = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    audio = np.array([np.sin(2 * np.pi * freq * t) for freq in frequencies]).sum(axis=0)

    # audio = abs(audio)
    audio /= np.max(np.abs(audio))


    # t2 = np.linspace(0, duration, 4000 * duration, endpoint=False)
    # audio2 = np.array([np.sin(2 * np.pi * freq * t2) for freq in frequencies]).sum(axis=0)
    # audio2 /= np.max(np.abs(audio2))

    plt.figure(figsize=(8, 4))
    plt.plot(t, audio, color='blue')
    # plt.plot(t2, audio2, color='red')
    plt.title('Generated Audio Waveform')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

    # Convert the audio to 16-bit samples
    # audio = np.int16(audio * 32767)

    # write('output_sound.wav', sample_rate, audio)

    sd.play(audio, sample_rate)
    sd.wait()


# generate_sound()

def test():
    sample_rate = 44100
    duration = 3
    frequencies = [1, 2, 3]
    t = np.linspace(0, 20, 3, endpoint=True)

    print(t)
    audio = np.array([np.sin(2 * np.pi * freq * t) for freq in frequencies]).sum(axis=0)
    # audio = np.array([(freq * t) for freq in frequencies]) .sum(axis=0)

    print()
    print(audio)



def generate_rand_sound():
    sample_rate = 10000
    duration = 3
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    audio = [random.randint(-1000, 1000) / 1000 for _ in range(len(t))]
    # audio = [np.sin(i * 1) for i in range(len(t))]

    # plt.plot(t, audio)
    # plt.show()

    sd.play(audio, sample_rate)
    sd.wait()


generate_rand_sound()

