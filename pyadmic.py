import pyaudio

def print_device_info():
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()

    print("Available audio devices:")
    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        print(device_info)
        print(f"{i}: {device_info['name']}")

    p.terminate()

def select_microphone(device_index):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=1024)

    print(f"Recording from {p.get_device_info_by_index(device_index)['name']}.")
    
    # Your recording or processing code goes here

    stream.stop_stream()
    stream.close()
    p.terminate()

# Print available audio devices
print_device_info()

# Select a specific microphone by providing its index
selected_device_index = 19  # Replace with the index of your desired microphone
select_microphone(selected_device_index)
