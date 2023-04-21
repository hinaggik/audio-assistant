import numpy as np
import matplotlib.pyplot as plt

def update_audio_meter(ax, indata, frames, time, status):
    data = np.frombuffer(indata, dtype=np.int16)
    data = np.array(data).flatten()
    y = (data.astype(float) / 2**15) * 100
    x = np.arange(len(y))
    ax.clear()
    ax.bar(x, y)
    ax.figure.canvas.draw()

def update_plot(ax, data):
    ax.clear()
    ax.imshow(data, cmap='coolwarm', aspect='auto', interpolation='nearest', extent=[0, len(data[0]), 0, 20])
    plt.pause(0.01)
