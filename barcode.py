import sys
import argparse
import cv2
import numpy as np

def averageColorPerRow(image):
    a =  np.average(image, axis=1)
    return a[:, np.newaxis, :]

def convert(inputfile, outputfile, fps):
    vid = cv2.VideoCapture(inputfile)
    length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    vidHeight = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) )

    columns = [] #Will hold bgr formatted columns of output image

    success, image = vid.read()
    while success:
        columns.append(averageColorPerRow(image))
        
        print("Progress: {}/{} ({:.1f}%)".format(len(columns), length, (100*len(columns)/length)), end="\r")
        success, image = vid.read()

    #Assemble columns and save image:
    cv2.imwrite(outputfile, cv2.hconcat(columns))
    print("\nImage saved to {}!".format(outputfile))

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0 or args[0] in ["--help", "-h"]:
        #Print help page
        print("""barcode.py

Usage:
    barcode.py <inputfile> [outputfile] [--fps=<fps>]
    barcode.py -h | --help

Options:
    -h --help     Show this information
    [outputfile]  Set output filename
    --fps=<fps>   How many frames to sample from each second of video

Examples:
    barcode.py video.mp4 out.png --fps=4""")
    else:
        parser = argparse.ArgumentParser()

        parser.add_argument("inputfile", type=str)
        parser.add_argument("outputfile", type=str, nargs='?', default="output.png")
        parser.add_argument("--fps", type=int, default=0)

        pArgs = parser.parse_args()
        convert(pArgs.inputfile, pArgs.outputfile, pArgs.fps)
