import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set up the plot
fig, ax = plt.subplots()
x = np.arange(0, 1000, 1)
line, = ax.plot(x, np.zeros_like(x))

# Set up the microphone input stream
chunk_size = 1000
sample_format = pyaudio.paInt16
channels = 1
sample_rate = 44100

p = pyaudio.PyAudio()
stream = p.open(format=sample_format,
                channels=channels,
                rate=sample_rate,
                frames_per_buffer=chunk_size,
                input=True)

# Variable to check if space key is pressed
space_pressed = False

def on_key(event):
    global space_pressed
    if event.key == ' ':
        space_pressed = True

# Attach the key press event handler
fig.canvas.mpl_connect('key_press_event', on_key)

def update_plot(frame):
    global space_pressed

    # Read microphone input
    audio_data = np.frombuffer(stream.read(chunk_size), dtype=np.int16)

    # Update the plot with the new waveform
    line.set_ydata(audio_data)

    # Check if space key is pressed to close the plot
    if space_pressed:
        plt.close(fig)

    return line,

# Set up the animation
ani = FuncAnimation(fig, update_plot, blit=True)

# Show the live waveform plot
plt.show()

# Stop the microphone stream when the plot is closed
stream.stop_stream()
stream.close()
p.terminate()
