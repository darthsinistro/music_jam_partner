# Part 1: Read audio
# Part 1a: Read audio from audio file
import os
import matplotlib.pyplot as plt
import librosa, librosa.display

#Load Audio file
audio_file = 'audio_samples/g_gmaj7.wav'
g_chords, sr = librosa.load(audio_file)

# Part 2: Setup FT
import numpy as np

# Define the number of samples I'll be using in each frame
FRAME_DURATION = 1 # Number of seconds for a frame
FRAME_SIZE = int(sr*FRAME_DURATION)
print(f'Number of frames: {int(np.ceil(len(g_chords)/FRAME_SIZE))}')

# Part 3: Visualize Frequency domain

def plot_magnitude_spectrum(signal, sr, title, frame_num = 1, f_ratio=1):
    sample = signal[(frame_num-1)*FRAME_SIZE:frame_num*FRAME_SIZE]
    X = np.fft.fft(sample)
    X_mag = np.absolute(X)
    
    plt.figure(figsize=(18, 5))
    
    f = np.linspace(0, sr, len(X_mag))
    f_bins = int(len(X_mag)*f_ratio)  
    
    plt.plot(f[:f_bins], X_mag[:f_bins])
    plt.xlabel('Frequency (Hz)')
    plt.title(title)
    plt.show()

plot_magnitude_spectrum(g_chords, sr, "G Chords", 10, 0.025)

# Part 3a: Identify notes
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def freq_to_number(f):
    return (69 + 12*np.log2(f/440.0))

def number_to_freq(n):
    return (440 * 2.0**((n-69)/12.0))

def note_name(n):
    return (NOTE_NAMES[n % 12])



# Part 4: Identify chord from notes