#!//usr/bin/python3


"""
the aim of this script is to give different views of muscic sounds
this script is inspired from the Snail (IRCAM) and from
https://github.com/markjay4k/Audio-Spectrum-Analyzer-in-Python/blob/master/spec_anim.py
"""


import os
import sys
import pyaudio
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from math import log, pi, cos, sin
from matplotlib import animation
from matplotlib.patches import Circle
from scipy.fftpack import fft
from scipy.signal import find_peaks


CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
AMPLITUDE_LIMIT = 4096
AUTOTUNE = True


def init_audio():
    """ initialisation of audio stream """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK)
    return p, stream


def init_axes(ax1, ax2, ax3):
    """ initialisation of axes style """
    ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
    ax1.set_xlim(0, 2 * CHUNK)
    ax1.set_axis_off()

    ax2.set_xlim(20, RATE / 2)
    ax2.get_yaxis().set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(True)
    ax2.spines['left'].set_visible(False)
    ax2.set_xlim(55., 3520.)

    ax3.set_xlim(-1.4, 1.4)
    ax3.set_ylim(-1.4, 1.4)
    ax3.set_axis_off()
    x_list = list()
    y_list = list()
    for index in range(601):
        angle = ((index - 300.) / 100.) * 2. * pi
        radius = 1. + 0.1 * angle / (2. * pi)
        x_list.append(radius * sin(angle))
        y_list.append(radius * cos(angle))
    ax3.plot(x_list, y_list, 'w-', lw=1)
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    for index in range(13):
        x_list = list()
        y_list = list()
        angle = (index / 12.) * 2. * pi
        radius = 0.7 + 0.1 * angle / (2. * pi)
        x_list.append(radius * sin(angle))
        y_list.append(radius * cos(angle))
        radius = 1.2 + 0.1 * angle / (2. * pi)
        x_list.append(radius * sin(angle))
        y_list.append(radius * cos(angle))
        ax3.plot(x_list, y_list, 'w-', lw=1)
        if index > 0 :
            plt.text(1.1 * x_list[-1], 1.1 * y_list[-1],
                     notes[index % 12],
                     rotation = -(180./pi) * angle,
                     ha='center', va='center')


def init_plot():
    """ initialisation of plots """
    plt.style.use('dark_background')
    figure = plt.figure("snail", figsize=(16, 8))
    ax1 = plt.subplot(1, 3, 1)
    x = np.arange(0, 2 * CHUNK, 2)
    wave_form, = ax1.plot(x, np.random.rand(CHUNK), 'w-', lw=2)
    ax2 = plt.subplot(1, 3, 2)
    xf = np.linspace(0, RATE, CHUNK)
    spectrum, = ax2.semilogx(xf, np.random.rand(CHUNK), 'w-', lw=2)
    peaks, = ax2.semilogx([], [], 'ro')
    ax3 = plt.subplot(1, 3, 3, aspect='equal')
    init_axes(ax1, ax2, ax3)
    return figure, wave_form, spectrum, peaks, ax3


def on_close(evt):
    """ close audio stream when application is shut down """
    print("Closing")
    STREAM.stop_stream()
    STREAM.close()
    P.terminate()
    print('stream stopped')
    quit()


def compute_snail(peak_frequencies, peak_amplitudes):
    """ computute angle, radius and size from frequencies """
    x_list = list()
    y_list = list()
    radius_list = list()
    for index in range(len(peak_frequencies)):
        a_frequency = peak_frequencies[index]
        if a_frequency < (RATE / 2):
            half_tons = 12. * log(a_frequency / 440.) / log(2.)
            if AUTOTUNE:
                angle = (2. * pi / 12.) * round(half_tons)
            else:
                angle = (2. * pi / 12.) * half_tons
            radius = 1. + 0.1 * angle / (2. * pi)
            angle = angle % (2. * pi)
            x_list.append(radius * sin(angle))
            y_list.append(radius * cos(angle))
            radius_list.append(0.2 * peak_amplitudes[index])
    return x_list, y_list, radius_list


def animate(i):
    """ animation function """
    data = STREAM.read(CHUNK)
    data_np = np.frombuffer(data, dtype='h')
    wave_form.set_ydata(data_np)
    yf = fft(data_np)
    spectrum_amplitudes = np.abs(yf[0:CHUNK]) / (512 * CHUNK)
    spectrum_peaks = find_peaks(spectrum_amplitudes,
                                threshold = 0.02)
    ax3.patches = []
    if len(spectrum_peaks[0]) > 0:
        new_peaks = list()
        peak_amplitudes = list()
        for index in spectrum_peaks[0]:
            candidate = index
            if spectrum_amplitudes[index - 1] > spectrum_amplitudes[index]:
                candidate = index - 1
            if spectrum_amplitudes[index + 1] > spectrum_amplitudes[index]:
                candidate = index + 1
            new_peaks.append(RATE / CHUNK * candidate)
            peak_amplitudes.append(spectrum_amplitudes[candidate])
        peak_frequencies = new_peaks
        peaks.set_data(peak_frequencies, peak_amplitudes)
        x_list, y_list, radius_list = compute_snail(peak_frequencies,
                                                    peak_amplitudes)
        for index in range(len(radius_list)):
            ax3.add_patch(Circle(xy=(x_list[index], y_list[index]),
                                 radius=radius_list[index],
                                 facecolor="red"))
    else:
        peaks.set_data([], [])
    spectrum.set_ydata(spectrum_amplitudes)


if __name__ == '__main__':
    print('stream started')
    P, STREAM = init_audio()
    figure, wave_form, spectrum, peaks, ax3 = init_plot()
    anim = animation.FuncAnimation(figure, animate, blit=False, interval=1)
    figure.canvas.mpl_connect('close_event',  on_close)
    plt.show()
