"""
Name:           Carlos Meza
Date:           02/25/19
"""

import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import freqz

""" READ FILE """
data, samplerate = sf.read('P_9_2.wav')

""" CONSTANTS """
L = 101
M = L - 1
fc = 7500 # in HZ
fr = np.ones(L)

# Produce h[n] values of 1 for default
H = np.ones(M)
W = np.ones(M)
HW = np.ones(M)

""" FUNCTIONS """
# Function for the low Pass Filter
def low_pass(n):
    ft = fc / samplerate
    # Determine filter weights
    if(n != (M/2)):
        filter_weight = np.sin(2 * np.pi * ft * (n - M/2)) / (np.pi * (n - M/2))
    else:
        filter_weight = 2 * ft
    # Return weight
    return filter_weight

def windowing(n):
    # Create w(n) value
    window = 0.54 - 0.46 * np.cos((2*np.pi*n)/M)
    return window

# Populate frequency array
for i in range(M):
    H[i] = low_pass(i)
    
# Get frequency response before applying window
x, y = freqz(H, 1)
plt.plot(x, abs(y))

# Populate window array
for k in range(M):
    W[k] = windowing(k)
    
# Apply filter coefficients to produce h[n]
HW = np.multiply(H, W)

# Plot the frequency response of h[n]
x, y = freqz(HW, 1)
plt.plot(x, abs(y))

# Output new song without fuzz
clean_file = np.convolve(data, HW)
sf.write('cleanMusic.wav', clean_file, samplerate)
