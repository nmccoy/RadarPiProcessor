import pyaudio
import numpy
import matplotlib.pyplot as plt
import time
import pygame
import sys
from pygame.locals import *
import csv

visuals = True
dualChannel = True
verbose = True
logging = True

#Display
RESOLUTION = ( 1280, 1024 )
#RESOLUTION = ( 500, 400 )
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Parameters
chunk=1024*16
c=299e6
Fc=2.4e9
Fs=44100
nfft=20000
numRows=200

#Initialize graph
#X = range(nfft/2)
#Y = [x*10 for x in X]
#plt.ion()
#graph = plt.plot(X,Y)[0]

def debug(debugStr):
	if(verbose):
		print debugStr

# Initialize gui and return a screen
def start_gui():
	pygame.init()
	screen = pygame.display.set_mode(RESOLUTION)
	pygame.display.set_caption('Hello world!')
	pygame.mouse.set_visible(False)
	update_speed(screen,0)
	return screen
	
def update_speed(screen,speed):
	# set up fonts
	basicFont = pygame.font.Font(None, 300)
	smallFont = pygame.font.Font(None, 100)
	# set up the text       
	speedText = basicFont.render(str(speed), True, BLUE)
	msText = smallFont.render('meters/sec',True,BLUE)
	textRect = speedText.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery
	msRect = msText.get_rect()
	msRect.centerx = screen.get_rect().centerx
	msRect.centery = screen.get_rect().centery+300
	# draw the white background onto the surface
	screen.fill(WHITE)
	# draw the text onto the surface
	screen.blit(speedText, textRect)
	screen.blit(msText,msRect)
	# draw the window onto the screen
	pygame.display.update()

def gui_loop():
	for event in pygame.event.get():
		if event.type == QUIT:
		    pygame.quit()
		    sys.exit()
#Initialize PyAudio
debug("Initializing Audio")
pyaud = pyaudio.PyAudio()
debug("Audio Initialized")


#Start GUI
if(visuals):
	debug("Starting GUI")
	screen = start_gui()
	debug("GUI Started")

# Open input stream, 16-bit stereo at 44100 Hz
if(dualChannel):
	defChans = 2
else:
	defChans = 1
stream = pyaud.open(
	format = pyaudio.paInt16,
	channels = defChans,
	rate = Fs,
#       input_device_index = 2, # Automatically picks one if commented
	input = True,
	frames_per_buffer = chunk)

print "Opened microphone"

##for x in range(0,5):
##        data = stream.read(chunk)
##        print "butts"

#screen=start_gui()
keepGoing=True
threshVals=None
#plt.show()
#time.sleep(3)
while keepGoing:
	data = stream.read(chunk)
	decoded = numpy.fromstring(data,dtype=numpy.int16)
	if(dualChannel):
		left = decoded[0::2]
	else:
		left = decoded

	fftData = numpy.absolute(numpy.fft.fft(left,nfft))[0:nfft/2]
	fftFreqs = numpy.fft.fftfreq(len(fftData)*2)

	peakIndex = numpy.argmax(fftData)
	maxVal = numpy.max(fftData)
	freqHz = fftFreqs[peakIndex]*Fs
	ms = int(round(time.time()*1000))
	if(threshVals == None):
		threshVals = fftData
	if(maxVal > threshVals[peakIndex]):
		velocityMetersSec = (freqHz*c)/(Fc)
	else:
		velocityMetersSec = 0.0
	if(verbose):
		print "   "+str(velocityMetersSec)+" m/s at " +str(ms)+" ms"
	if(visuals):
		update_speed(screen,"{0:.1f}".format(velocityMetersSec))
		gui_loop()
	if(logging):
		with open('log.csv','a') as csvfile:
			logwriter = csv.writer(csvfile)
			logwriter.writerow([velocityMetersSec,peakIndex]+fftData.tolist())
	keepGoing=True

print "Data accquired"
stream.stop_stream()
stream.close()
pyaud.terminate()
print "Stream closed"
#plt.plot(left)

#plt.plot(fftData)
#plt.show()


    
