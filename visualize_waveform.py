import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second
INPUT_DEVICE_ID = 2          # 2 for the laptop mic

# create matplotlib figure and axes
fig, ax = plt.subplots(figsize=(15, 7))

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=INPUT_DEVICE_ID,
    output=True,
    frames_per_buffer=CHUNK
)

# variable for plotting
x = np.arange(0, CHUNK)

# create a line object with random data
line, = ax.plot(x, x, '-', lw=2)
ax.set_ylim(-10000,10000)

# show the plot
plt.show(block=False)

while True:
    # binary data
    data = stream.read(CHUNK)
    
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(CHUNK) + 'h', data)
    data_np = np.array(data_int)
    
    line.set_ydata(data_np)
    plt.pause(0.001)