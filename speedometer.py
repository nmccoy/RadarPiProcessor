import pyaudio

#Initialize PyAudio
pyaud = pyaudio.PyAudio()

# Open input stream, 16-bit stereo at 4410 Hz
stream = pyaud.open(
	format = pyaudio.paInt16,
	channels = 2,
	rate = 44100,
	input_device_index = 2,
	input = True)
 
