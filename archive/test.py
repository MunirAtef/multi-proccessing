
import numpy as np
from pydub import AudioSegment
import librosa

# Function to generate random audio
def generate_audio(duration=5, sampling_rate=44100):
    # Generate random noise
    noise = np.random.normal(0, 0.5, int(sampling_rate * duration))

    # Convert the numpy array to an AudioSegment
    audio = AudioSegment(
        noise.tobytes(),
        frame_rate=sampling_rate,
        sample_width=noise.dtype.itemsize,
        channels=1
    )


# Function to save audio to file
def save_audio(audio, filename="output.wav"):
    audio.export(filename, format="wav")

# Function to load and visualize audio
def visualize_audio(filename="output.wav"):
    y, sr = librosa.load(filename)
    librosa.display.waveshow(y, sr=sr)


# Generate audio
gen_audio = generate_audio()
print(gen_audio)

# Save the generated audio to a file
# save_audio(gen_audio)

# Visualize the generated audio
# visualize_audio()



# if __name__ == '__main__':
#     print()
