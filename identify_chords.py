# Part 1: Read audio
# Part 1a: Read audio from audio file
import os
import matplotlib.pyplot as plt
import librosa, librosa.display

audio_file = 'G:/My Drive/Box Sync/Analytics/music_jam_partner/audio_samples/g_gmaj7.wav'

g_chords, sr = librosa.load(audio_file)

# Part 2: Perform FT
import numpy as np
FRAME_DURATION = 0.25 # Number of seconds for a frame
FRAME_SIZE = int(2**np.floor(np.log2(sr*FRAME_DURATION)))
HOP_SIZE = int(FRAME_SIZE/4)

g_stft = librosa.stft(g_chords, n_fft=FRAME_SIZE, hop_length=HOP_SIZE)

# Part 3a: Visualize STFT spectrogram
Y_scale = np.abs(g_stft) ** 2

def plot_spectrogram(Y, sr, hop_length, y_axis="linear"):
    plt.figure(figsize=(25, 10))
    librosa.display.specshow(Y, 
                             sr=sr, 
                             hop_length=hop_length, 
                             x_axis="time", 
                             y_axis=y_axis)
    plt.colorbar(format="%+2.f")
    plt.show()

Y_log_scale = librosa.power_to_db(Y_scale)
plot_spectrogram(Y_log_scale, sr, HOP_SIZE, y_axis="log")
plot_spectrogram(Y_log_scale, sr, HOP_SIZE, y_axis="linear")

lst_freq = librosa.fft_frequencies(sr=sr, n_fft=FRAME_SIZE)

def plot_magnitude_spectrum_time(Y, lst_freq, frame_idx=0, f_ratio=1):
    plt.figure(figsize=(25, 10))
    f_bins = int(f_ratio*len(lst_freq))
    plt.plot(lst_freq[:f_bins],Y[:f_bins,frame_idx])
    plt.xlabel('Frequency (Hz)')
    plt.show()

plot_magnitude_spectrum_time(Y_log_scale, lst_freq, 100, f_ratio=0.2)

# Part 3a: Visualize Frequency domain

def plot_magnitude_spectrum(signal, sr, title, f_ratio=1):
    X = np.fft.fft(signal)
    X_mag = np.absolute(X)
    
    plt.figure(figsize=(18, 5))
    
    f = np.linspace(0, sr, len(X_mag))
    f_bins = int(len(X_mag)*f_ratio)  
    
    plt.plot(f[:f_bins], X_mag[:f_bins])
    plt.xlabel('Frequency (Hz)')
    plt.title(title)
    plt.show()

plot_magnitude_spectrum(g_chords[:int(g_chords.shape[0]/3)], sr, "G Chords", 0.025)

# Part 3a: Identify notes
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def freq_to_number(f):
    return (69 + 12*np.log2(f/440.0))

def number_to_freq(n):
    return (440 * 2.0**((n-69)/12.0))

def note_name(n):
    return (NOTE_NAMES[n % 12])



# Part 4: Identify chord from notes