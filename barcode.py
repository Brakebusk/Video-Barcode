import cv2
import numpy as np

vid = cv2.VideoCapture('video.mp4')
length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

vidHeight = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) )
output = np.empty(vidHeight)

def averageColorPerRow(image):
    return np.average(image, axis=1)    

success, image = vid.read()
count = 0
while success:
    count += 1
    
    colorAverage = averageColorPerRow(image)
    output = np.column_stack((output, colorAverage))
    print("Progress: {}/{} ({:.1f}%)".format(count, length, (100*count/length)), end="\r")
    success, image = vid.read()

cv2.imwrite("output.png", output)
