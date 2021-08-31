import seaborn as sns
import numpy as np
from object import object
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib
import time

class heap:

    ROOT = object(address=-1, child=None, size=0)
    FREE = object(address=0, child=None, size=0)

    def __init__(self, size):
        self.size = size
        self.space_mark = np.zeros((size, ))
        self.space_ = {}
        self.space_[0] = self.FREE
        self.FREE.size = size

    def heatmap(self):
        length = np.sqrt(self.size)
        length = int(length)
        width = int(np.ceil(self.size / length))
        space = self.space_mark
        if length * width - self.size > 0:
            padding = np.zeros((length * width - self.size, )) + -1
            space = np.append(self.space_mark, padding)
        space = space.reshape((length, width))
        ax = sns.heatmap(space, vmax=1.0, vmin=-1.0, linewidths=0.5, linecolor="Black", cmap="Blues")
        self.annotate_heatmap(ax, data=space ,valfmt="{x:d}")
        plt.show()

    def annotate_heatmap(self, im, data=None, valfmt="{x:.2f}",
                         textcolors=("black", "white"),
                         threshold=None, **textkw):

        if not isinstance(data, (list, np.ndarray)):
            data = im.get_array()

        # Set default alignment to center, but allow it to be
        # overwritten by textkw.
        kw = dict(ha="center",
                  va="center",
                  color="black")
        kw.update(textkw)

        # Get the formatter in case a string is supplied
        if isinstance(valfmt, str):
            valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

        # Loop over the data and create a `Text` for each "pixel".
        # Change the text's color depending on the data.
        texts = []
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                text = im.axes.text(j+0.5, i+0.5, valfmt(i*data.shape[1] + j, None), **kw)
                texts.append(text)

        return texts