# Part 1: Read audio
# Part 1a: Read audio from audio file
import os
import matplotlib.pyplot as plt
import librosa, librosa.display

#Load Audio file
audio_file = 'audio_samples/mtw.wav'
wav_audio, sr = librosa.load(audio_file)

# Part 2: Setup FT
import numpy as np

# Define the number of samples I'll be using in each frame
FRAME_DURATION = 1 # Number of seconds for a frame
FRAME_SIZE = int(sr*FRAME_DURATION)
print(f'Number of frames: {int(np.ceil(len(wav_audio)/FRAME_SIZE))}')

# Part 3: Visualize and extract Frequency domain

def plot_magnitude_spectrum(signal, sr, title, plot_diag=True, frame_num = 1, f_ratio=1, list_thresh=100):
    sample = signal[(frame_num-1)*FRAME_SIZE:frame_num*FRAME_SIZE]
    X = np.fft.fft(sample)   # TODO: include hanning window here?
    X_mag = np.absolute(X)
    
    f = np.linspace(0, sr, len(X_mag))
    f_bins = int(len(X_mag)*f_ratio)  
    if plot_diag:
        plt.figure(figsize=(18, 5))
        plt.plot(f[:f_bins], X_mag[:f_bins])
        plt.xlabel('Frequency (Hz)')
        plt.title(title)
        plt.show()

    unsort_freq = list(zip(f[:f_bins], X_mag[:f_bins]))
    unsort_freq = [(freq,amp) for freq, amp in unsort_freq if amp >= list_thresh]
    sorted_freq = sorted(unsort_freq, key=lambda item: item[1], reverse=True)
    return sorted_freq

freq_list = plot_magnitude_spectrum(wav_audio, sr, "G Chords", plot_diag=False,
                                    frame_num=12, f_ratio=0.025)  #Look at the 5th and 12th frames at 1 second definition

# Part 3a: Identify notes
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def freq_to_number(f):
    return (69 + 12*np.log2(f/440.0))

def number_to_freq(n):
    return (440 * 2.0**((n-69)/12.0))

def note_name(n):
    return (NOTE_NAMES[n % 12])

def get_notes(freq_list):
    idx = 0
    found_notes = []
    while (idx<len(freq_list)):
        f = freq_list[idx][0]
        n = freq_to_number(f)
        n0 = int(round(n))
        name = note_name(n0)

        if name not in found_notes:
            found_notes.append(name)
        idx += 1
    return found_notes

get_notes(freq_list)


for cur_frame in range(int(np.ceil(len(wav_audio)/FRAME_SIZE))):
    cur_freq_list = plot_magnitude_spectrum(wav_audio, sr, "G Chords", plot_diag=False,
                                    frame_num=(cur_frame+1), f_ratio=0.025)
    print(f'Notes in frame {cur_frame+1} are: {get_notes(cur_freq_list)}')

# Part 4: Identify chord from notes
import csv
from collections import deque

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data


#Let's read in the file with the chord formula and create a dictionary
chord_path = 'chordFormula/chords.csv'
chord_data = read_csv_file(chord_path)
chord_dict = {chord_row[4]:chord_row[0] for chord_row in chord_data[1:]}


# Now a function that inputs a set of notes and returns the possible chord names
def chord_from_notes(notes_list):
    chromatic_scale = deque(NOTE_NAMES)

    possible_chords = []

    for cur_note in notes_list:
        chromatic_scale.rotate(-chromatic_scale.index(cur_note))
        temp_formula = '-'.join(sorted([str(chromatic_scale.index(ind_note)) for ind_note in notes_list]))
        if temp_formula in chord_dict.keys():
            possible_chords.append(cur_note + " " + chord_dict[temp_formula])
    
    return possible_chords

notes_list = ['D', 'G', 'B'] # Delete when done testing
chord_from_notes(notes_list)