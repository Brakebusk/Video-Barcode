import sys
import argparse
import cv2
import numpy as np

def averageColorPerRow(image):
    a =  np.average(image, axis=1)
    return a[:, np.newaxis, :]

def convert(inputfile, outputfile, sps):
    vid = cv2.VideoCapture(inputfile)
    length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    framerate = int(vid.get(cv2.CAP_PROP_FPS))
    samplerate = int(framerate / sps) if sps > 0 else 1

    columns = [] #Will hold bgr formatted columns of output image

    counter = 0
    success, image = vid.read()
    while success:
        if counter % samplerate == 0:
            columns.append(averageColorPerRow(image))
        print("Progress: {}/{} ({:.1f}%)".format(counter, length, (100*counter/length)), end="\r")
        success, image = vid.read()
        counter += 1

    #Assemble columns and save image:
    cv2.imwrite(outputfile, cv2.hconcat(columns))
    print("\nImage saved to {}!".format(outputfile))

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0 or args[0] in ["--help", "-h"]:
        #Print help page
        print("""barcode.py

Usage:
    barcode.py <inputfile> [outputfile] [--sps=<sps>]
    barcode.py -h | --help

Options:
    -h --help     Show this information
    [outputfile]  Set output filename
    --sps=<sps>   Samples Per Second - How many frames to sample from each second of video

Examples:
    barcode.py video.mp4 out.png --sps=4""")
    else:
        parser = argparse.ArgumentParser()

        parser.add_argument("inputfile", type=str)
        parser.add_argument("outputfile", type=str, nargs='?', default="output.png")
        parser.add_argument("--sps", type=int, default=0)

        pArgs = parser.parse_args()
        convert(pArgs.inputfile, pArgs.outputfile, pArgs.sps)
