"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).
"""

import pyaudio
import wave
import numpy as np

CHUNK = 1024
WIDTH = 2
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

# use a Blackman window
window = np.blackman(CHUNK)

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("* recording")

data = stream.read(CHUNK)

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     stream.write(data, CHUNK)


while len(data) == CHUNK*WIDTH:
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/WIDTH),\
                                         data))*window
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/CHUNK
        print "The freq is %f Hz." % (thefreq)
    else:
        thefreq = which*RATE/CHUNK
        print "The freq is %f Hz." % (thefreq)
    # read some more data
    data = stream.read(CHUNK)
    if data:
        stream.write(data)

print("* done")

stream.stop_stream()
stream.close()

p.terminate()
