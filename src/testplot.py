# Generates an example 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def createTestPlot() -> Figure:
    # Create a sample matplotlib plot
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x) * 0.5
    y3 = y1 * y2

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.plot(x, y1, 'r-', linewidth=2, label='sin(x)')
    ax.plot(x, y2, 'b--', marker='o', markersize=2, 
            markevery=10, label='0.5*cos(x)')
    ax.plot(x, y3, 'g-', linewidth=3, marker='D', markersize=4, 
            markevery=5, label='0.5*cos(x) * sin(x)')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    ax.legend()

    return fig