import pyaudio
import numpy
import matplotlib.pyplot as plt
import time
import pygame
import sys
from pygame.locals import *

#Display
RESOLUTION = ( 1280, 1024 )
#RESOLUTION = ( 500, 400 )
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Parameters
chunk=1024*8
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

# Initialize gui and return a screen
def start_gui():
        pygame.init()
        screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption('Hello world!')
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
pyaud = pyaudio.PyAudio()

# Open input stream, 16-bit stereo at 44100 Hz
stream = pyaud.open(
        format = pyaudio.paInt16,
        channels = 2,
        rate = Fs,
#       input_device_index = 2, # Automatically picks one if commented
        input = True,
        frames_per_buffer = chunk)

print "Opened microphone"

##for x in range(0,5):
##        data = stream.read(chunk)
##        print "butts"

screen=start_gui()
keepGoing=True
threshVal=0
plt.show()
while keepGoing:
        data = stream.read(chunk)
        decoded = numpy.fromstring(data,dtype=numpy.int16)
        left = decoded[0::2]
        #right = decoded[1::2]
        #fftData = numpy.absolute(numpy.fft.fftshift(numpy.fft.fft(left,nfft)))
        fftData = numpy.absolute(numpy.fft.fft(left,nfft))[0:nfft/2]
        fftFreqs = numpy.fft.fftfreq(len(fftData)*2)
        #graph.set_ydata(fftData)
        #plt.draw()
        #plt.draw()
        peakIndex = numpy.argmax(fftData)
        maxVal = numpy.max(fftData)
        freqHz = fftFreqs[peakIndex]*Fs
#        print "Peak freq "+str(peakIndex) + " which is " + str(freqHz) + " Hz"
        ms = int(round(time.time()*1000))
        if(threshVal == 0):
                threshVal = maxVal*3
        if(maxVal > threshVal):
                velocityMetersSec = (freqHz*c)/(Fc)
        else:
                velocityMetersSec = 0.0
        #print "   "+str(velocityMetersSec)+" m/s at " +str(ms)+" ms"
        update_speed(screen,"{0:.1f}".format(velocityMetersSec))
        gui_loop()
        keepGoing=True

print "Data accquired"
stream.stop_stream()
stream.close()
pyaud.terminate()
print "Stream closed"
#plt.plot(left)

#plt.plot(fftData)
#plt.show()


    
