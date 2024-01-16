from BLF import BottomLeftFill
from genetic_algoritma import GA
from get_data import readFile
from shapes import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--ga', type=str, default="False")
    parser.add_argument('--gen_size', type=int, default=5)
    parser.add_argument('--pop_size', type=int, default=10)
    args = parser.parse_args()

    bin_width, bin_height, rectangles = readFile()

    if args.ga == "True":
        start = time.time()
        ga = GA(bin_width, bin_height, rectangles, args.gen_size, args.pop_size)
        result_list, result_density, bin = ga.genetic_algorithm()
        stop = time.time()
        print(f"Yogunluk: {result_density}")
        print(f"Sure: {stop - start}")

    else:
        bin = Bin(bin_width, bin_height)
        blf = BottomLeftFill(bin, rectangles)
        blf.place()
        print(f"Yogunluk: {blf.density}")

    fig, ax = plt.subplots(figsize=(15, 10))
    for patch in bin.placement:
        ax.add_patch(patches.Rectangle(patch[0], patch[1][0], patch[1][1], linewidth=1, edgecolor='black', facecolor='red'))

    plt.xlim(0, bin_width)
    plt.ylim(0, bin_height)

    plt.xticks(range(0, bin_width + 1, 4))
    plt.yticks(range(0, bin_height + 1, 4))  

    #plt.gca().invert_yaxis()
    plt.show()