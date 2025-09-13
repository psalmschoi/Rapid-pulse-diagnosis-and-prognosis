from core.Data import Data
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def plot_single_pulse(path, ID):
    cell = Data(path, ID)
    cell.get_Peak()

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    ax_flat = axes.flatten()

    cmap = cm.inferno
    colors = [cmap(i) for i in np.linspace(0, 1, cell.Result.shape[1])] 

    for c_rate_idx, set in enumerate(cell.Result):
        c_rate = "0.5C" if c_rate_idx else "0.1C"
        ax = ax_flat[c_rate_idx]
        ax.set_title(f"Set {c_rate}")
        for time_idx, points in enumerate(set):
            ax.plot(points, color=colors[time_idx])

    plt.show()


if __name__ == '__main__':
    plot_single_pulse("DMM", 8)