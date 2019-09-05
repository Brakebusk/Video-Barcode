import cv2
import numpy as np

vid = cv2.VideoCapture('video.mp4')
length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

vidHeight = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) )
output = np.empty([vidHeight, 0, 3])

def averageColorPerRow(image):
    a =  np.average(image, axis=1)
    return a[:, np.newaxis, :]


success, image = vid.read()
count = 0
while success:
    count += 1
    
    colorAverage = averageColorPerRow(image)
    output = cv2.hconcat([output, colorAverage])
    
    print("Progress: {}/{} ({:.1f}%)".format(count, length, (100*count/length)), end="\r")
    success, image = vid.read()

cv2.imwrite("output.png", output)
print("Image saved to output.png!")
