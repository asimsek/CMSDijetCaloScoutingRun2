import sys
import ROOT
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import argparse
import numpy as np
import copy


def yaxis_sci_format(power_of_ten):
    def formatter(x, pos):
        if x == 0:
            return '0'
        return "{:.0f}".format(x / 10**power_of_ten)
    return formatter


def read_root_data(filename):
    file = ROOT.TFile(filename, "READ")

    tree = file.Get("limit")

    r_values = []
    y_values = []
    for entry in tree:
        if entry.quantileExpected > -1.5:
            r_values.append(entry.r)
            y_values.append(2 * (entry.deltaNLL + entry.nll + entry.nll0))

    return r_values, y_values



def plot_data(filename, label, color, markersize=8):
    r_values, y_values = read_root_data(filename)
    plt.plot(r_values, y_values, label=label, color=color, linestyle='None', marker='o', markersize=markersize)



def main(args):
    plt.figure(figsize=(8, 8))

    files = args.f.split(',')
    labels = args.l.split(',')
    colors = args.c.split(',')



    for idx, (filename, label, color) in enumerate(zip(files, labels, colors)):
        if idx == len(files) - 1:  # Check if it's the last iteration
            plot_data(filename, label, color, markersize=5)
        else:
            plot_data(filename, label, color)


    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    y_label = plt.ylabel("-2lnL(r)+c", fontsize=18, fontweight='bold')
    x_label = plt.xlabel("r", fontsize=18, fontweight='bold')

    y_label.set_position((y_label.get_position()[0], 0.90))
    x_label.set_position((0.95, x_label.get_position()[1]))

    ax = plt.gca()
    ax.yaxis.offsetText.set_fontsize(18)

    plt.legend(numpoints=1, loc='upper left', fontsize=18)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.title("")
    plt.tight_layout()  # Ensure that labels and titles fit within the figure
    plt.savefig(args.o)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--f", type=str, help="Comma-separated list of root file paths.")
    parser.add_argument("--l", type=str, help="Comma-separated list of legend labels for each root file.")
    parser.add_argument("--c", type=str, help="Comma-separated list of colors for each plot.")
    parser.add_argument("--o", type=str, help="Name of the output PDF file.")

    args = parser.parse_args()
    main(args)




