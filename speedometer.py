import pyaudio
import numpy
import matplotlib.pyplot as plt

#Parameters
c=299e6
Fc=2.4e9
Fs=44100
nfft=2000
numRows=200

#Initialize PyAudio
pyaud = pyaudio.PyAudio()

# Open input stream, 16-bit stereo at 44100 Hz
stream = pyaud.open(
	format = pyaudio.paInt16,
	channels = 2,
	rate = Fs,
#	input_device_index = 2, # Automatically picks one if commented
	input = True)

print "Opened microphone"

keepGoing=True
while keepGoing:
	data = stream.read(Fs/4)
	decoded = numpy.fromstring(data,dtype=numpy.int16)
	left = decoded[0::2]
	#right = decoded[1::2]
	fftData = numpy.absolute(numpy.fft.fftshift(numpy.fft.fft(left,nfft)))
	keepGoing=False
	

print "Data accquired"
stream.stop_stream()
stream.close()
pyaud.terminate()
print "Stream closed"
#plt.plot(left)

plt.plot(fftData)
plt.show()
