import sys
import cv2
import numpy as np

def averageColorPerRow(image):
    a =  np.average(image, axis=1)
    return a[:, np.newaxis, :]

def convert(inputfile, outputfile="output.png"):
    vid = cv2.VideoCapture(inputfile)
    length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

    vidHeight = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) )
    output = np.empty([vidHeight, 0, 3])

    success, image = vid.read()
    count = 0
    while success:
        count += 1
        
        colorAverage = averageColorPerRow(image)
        output = cv2.hconcat([output, colorAverage])
        
        print("Progress: {}/{} ({:.1f}%)".format(count, length, (100*count/length)), end="\r")
        success, image = vid.read()

    cv2.imwrite(outputfile, output)
    print("\nImage saved to {}!".format(outputfile))

if __name__ == "__main__":
    try:
        inputfile = sys.argv[1]
        if len(sys.argv) > 2:
            convert(inputfile, sys.argv[2])
        else:
            convert(inputfile)

    except IndexError:
        print("Too few command line arguments given. Usage: barcode.py <videofile> [outputfile]")
