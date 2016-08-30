import pyaudio
import numpy
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import time
import pygame
import pylab
import sys
from pygame.locals import *
import csv

visuals = True
dualChannel = True
verbose = False
logging = False

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
nfftKeep=500
numRows=200

#Thresholding
threshValCount = 0
threshValCountDesired = 5
threshValScalar = 1

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
	textRect.centery = screen.get_rect().centery-150
	msRect = msText.get_rect()
	msRect.centerx = screen.get_rect().centerx
	msRect.centery = screen.get_rect().centery
	# draw the white background onto the surface
	screen.fill(WHITE)
	# draw the text onto the surface
	screen.blit(speedText, textRect)
	screen.blit(msText,msRect)

def update_hz(screen,freq):
	# set up fonts
	basicFont = pygame.font.Font(None, 300)
	smallFont = pygame.font.Font(None, 100)
	# set up the text       
	freqText = basicFont.render(str(freq), True, BLUE)
	hzText = smallFont.render('Hz',True,BLUE)
	textRect = freqText.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+200
	hzRect = hzText.get_rect()
	hzRect.centerx = screen.get_rect().centerx
	hzRect.centery = screen.get_rect().centery+350
	# draw the text onto the surface
	screen.blit(freqText, textRect)
	screen.blit(hzText,hzRect)


def gui_loop():
	for event in pygame.event.get():
		if event.type == QUIT:
		    pygame.quit()
		    sys.exit()

def plot_graph(screen,xaxis,yaxis):
	fig = pylab.figure(figsize=[RESOLUTION[0]/128,RESOLUTION[1]/128/2],dpi=128)
	ax = fig.gca()
	ax.plot(xaxis,yaxis)
	canvas = agg.FigureCanvasAgg(fig)
	canvas.draw()
	renderer = canvas.get_renderer()
	raw_data = renderer.tostring_rgb()
	size = canvas.get_width_height()
	surf = pygame.image.fromstring(raw_data,size,"RGB")
	screen.blit(surf,(0,0))
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
crashNum = 0
while keepGoing:
	try:
		data = stream.read(chunk)
	except:
		crashNum += 1
		print "Crash! #"+str(crashNum)
		continue
	decoded = numpy.fromstring(data,dtype=numpy.int16)
	if(dualChannel):
		left = decoded[0::2]
	else:
		left = decoded

	fftData = numpy.absolute(numpy.fft.fft(left,nfft))[0:nfftKeep]
	fftFreqs = numpy.fft.fftfreq(nfft)[0:nfftKeep]


	peakIndex = numpy.argmax(fftData)
	maxVal = numpy.max(fftData)
	freqHz = fftFreqs[peakIndex]*Fs
	ms = int(round(time.time()*1000))
	if(threshValCount < threshValCountDesired):
		if threshVals == None:	
			threshVals = fftData*threshValScalar
		else:
			threshVals += fftData*threshValScalar
		threshValCount += 1
	if(maxVal > threshVals[peakIndex]):
		velocityMetersSec = (freqHz*c)/(Fc)
	else:
		velocityMetersSec = 0.0
	if(verbose):
		print "   "+str(velocityMetersSec)+" m/s at " +str(ms)+" ms"
	if(visuals):
		update_speed(screen,"{0:.1f}".format(velocityMetersSec))
		#update_hz(screen,freqHz)
		#plot_graph(screen,fftFreqs*Fs*c/Fc,fftData)
		pygame.display.update()
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


    
