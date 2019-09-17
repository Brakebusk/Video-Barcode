from functools import reduce
import numpy as np
import argparse
import random
import sys
import cv2
import re

def averageColorPerRow(image, crop):
    a = np.average(image[crop[0]:crop[2],crop[3]:crop[1]], axis=1)
    return a[:, np.newaxis, :]

def autoCrop(inputfile):
    print("Autocropping...")
    try:
        #Open video and skip forward 500 frames:
        vid = cv2.VideoCapture(inputfile)
        ok, image = vid.read()
        for i in range(500):
            ok, image = vid.read()

        cropTop = 0
        cropRight = len(image[0]) - 1
        cropBottom = len(image) - 1
        cropLeft = 0

        hcenter = int(len(image[0]) / 2)
        vcenter = int(len(image) / 2)

        while np.all(image[cropTop][hcenter] == 0):
            cropTop += 1
        while np.all(image[vcenter][cropRight] == 0):
            cropRight -= 1
        while np.all(image[cropBottom][hcenter] == 0):
            cropBottom -= 1
        while np.all(image[vcenter][cropLeft] == 0):
            cropLeft += 1
        
        return (cropTop, cropRight, cropBottom, cropLeft)
    except IndexError:
        print("Error! Unable to autocrop frame. Ignoring...")
        return (0, len(image[0]), len(image), 0)

def convert(inputfile, outputfile, sps=0, ar=None, ignore=0, autocrop=False):
    #Gather general video file information:
    vid = cv2.VideoCapture(inputfile)
    framerate = int(vid.get(cv2.CAP_PROP_FPS))
    length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT)) - (framerate * ignore)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)) #Vertical resolution of video
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))

    #Figure out how much to crop out of the frame: (remove letterboxing)
    crop = autoCrop(inputfile) if autocrop else (0, width, height, 0)
    height -= (crop[0] + (height - crop[2]))

    #Determine samplerate either by given aspect ratio or by given samples-per-second value:
    if not ar:
        samplerate = round(framerate / sps) if sps > 0 and sps <= framerate else 1
    else:
        ratio = reduce(lambda x, y : x / y, map(int, ar.split(":"))) #Oneliner yo
        samplerate = round(length / (ratio * height))

    columns = [] #Will hold bgr formatted columns of output image

    #Go through video frame by frame and sample every samplerate' frame:
    counter = 0
    ok, image = vid.read()
    while ok and counter <= length:
        if counter % samplerate == 0:
            columns.append(averageColorPerRow(image, crop))
        print("Progress: {}/{} ({:.1f}%)".format(counter, length, (100*counter/length)), end="\r")
        ok, image = vid.read()
        counter += 1

    #Assemble columns and save image:
    try:
        cv2.imwrite(outputfile, cv2.hconcat(columns))
    except:
        #Problem with given filename fallback on default:
        outputfile = "output_{}.png".format(''.join(str(random.randint(0, 9)) for _ in range(5)))
        cv2.imwrite(outputfile, cv2.hconcat(columns))
    print("\nImage saved to {}!".format(outputfile))

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0 or args[0] in ["--help", "-h"]:
        #Print help page
        print("""barcode.py

Usage:
    barcode.py <inputfile> [outputfile] [--sps=<sps>] | [--ar=<width:height>] [--ignore=<seconds>] [--autocrop]
    barcode.py -h | --help

Options:
    -h --help           Show this information
    [outputfile]        Set output filename
    --sps=<sps>         Samples Per Second - How many frames to sample from 
                        each second of video
    --ar=<width:height> Output image aspect ratio - Automatically determine sps
    --ignore=<seconds>  Ignore the last x seconds of the input video (crop out credits)
    --autocrop          Automatically crop out letterboxing and pillarboxing

Examples:
    barcode.py video.mp4 out.png --sps=4""")
    else:
        parser = argparse.ArgumentParser()

        def ar_pattern(s, pat=re.compile(r"^\d+[:]\d+$")):
            #Used to validate ar value as <number>:<number> and nothing else
            if not pat.match(s):
                raise argparse.ArgumentTypeError
            return s

        parser.add_argument("inputfile", type=str)
        parser.add_argument("outputfile", type=str, nargs='?', default="output.png")
        parser.add_argument("--sps", type=int, default=0)
        parser.add_argument("--ar", type=ar_pattern, default=None)
        parser.add_argument("--ignore", type=int, default=0)
        parser.add_argument("--autocrop", action="store_true")

        pArgs = parser.parse_args()
        convert(pArgs.inputfile, pArgs.outputfile, pArgs.sps, pArgs.ar, pArgs.ignore, pArgs.autocrop)
