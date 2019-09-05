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
    try:
        inputfile = sys.argv[1]
        if len(sys.argv) > 2:
            convert(inputfile, sys.argv[2])
        else:
            convert(inputfile)

    except IndexError:
        print("Too few command line arguments given. Usage: barcode.py <videofile> [outputfile]")
