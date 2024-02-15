from make_noise import *
import pickle

snr = 1/3
noise_ratio = 1 / (snr+1)
signal_ratio = 1 - noise_ratio

noise_values_list = []
for i in range(20):
    noise_values_list.append((make_noise() - 0.25) * 2*noise_ratio + 0.5*signal_ratio)

with open('noise_values_list.pkl', 'wb') as file:
    pickle.dump(noise_values_list, file)