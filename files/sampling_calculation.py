# ! https://www.kaggle.com/code/faressayah/signal-processing-with-python/notebook

import matplotlib.pyplot as plt
import numpy as np

# signal without noise
f = 5000 # Hz
t = np.linspace(0, 0.001, 1000)
x1 = np.sin(2 * np.pi * f * t)

# signal noise
np.random.seed(1234)
time_step = 0.001
period = 0.1
time_vec = np.arange(0, 1, time_step)

# sig2 = np.sin(2 * np.pi / period * time_vec)+ 0.5 * np.random.randn(time_vec.size)
x1 = np.sin(1 * np.pi / period * time_vec)+ 0.5 * np.random.randn(time_vec.size)

plt.figure(figsize=(6, 5))
plt.plot(time_vec, x1, label='Original signal')

# (2 * np.pi / period * time_vec)+ 0.5 * np.random.randn(time_vec.size)

# signal noise
# np.random.seed(1234)
# time_step = 0.02
# period = 5.
# time_vec = np.arange(0, 20, time_step)
# x1 = (np.sin(2 * np.pi / period * time_vec)
#        + 0.5 * np.random.randn(time_vec.size))
# plt.figure(figsize=(6, 5))
# plt.plot(time_vec, x1, label='Original signal')


s_rate = 200000 # Hz. sampling frequency should match the requirement of sampling theorem

T = 1 / s_rate
n = np.arange(0, 0.001 / T)
nT = n * T
x2 = np.sin(2 * np.pi * f * nT) # Since for sampling t = nT.

print(len(t))
print(len(nT))

plt.figure(figsize=(10, 8))
plt.suptitle(f"Sampling a Sine Wave of Fmax={f}Hz with fs={s_rate}Hz", fontsize=20)

plt.subplot(2, 2, 1)
plt.plot(t, x1, linewidth=3, label=f'SineWave of frequency {f} Hz')
plt.xlabel('time.', fontsize=15)
plt.ylabel('Amplitude', fontsize=15)
plt.legend(fontsize=10, loc='upper right')

plt.subplot(2, 2, 2)
plt.plot(nT, x2, 'ro', label=f'Sample marks after resampling at fs={s_rate}Hz')
plt.xlabel('time.', fontsize=15)
plt.ylabel('Amplitude', fontsize=15)
plt.legend(fontsize=10, loc='upper right')

plt.subplot(2, 2, 3)
markerline, stemlines, baseline = plt.stem(nT, x2, linefmt='grey', label=f'Sample after resampling at fs={s_rate}Hz')
# markerline.set_markerfacecolor('none')
plt.xlabel('time.', fontsize=15)
plt.ylabel('Amplitude', fontsize=15)
plt.legend(fontsize=10, loc='upper right')

plt.subplot(2, 2, 4)
plt.plot(nT, x2, 'g-', label='Reconstructed Sine Wave')
plt.xlabel('time.', fontsize=15)
plt.ylabel('Amplitude', fontsize=15)
plt.legend(fontsize=10, loc='upper right')

plt.tight_layout()
plt.show()