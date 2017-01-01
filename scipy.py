from pylab import*
from scipy.io import wavfile

sampFreq, snd = wavfile.read('output.wav')

print(snd.dtype)
