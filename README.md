# Video-Barcode
It's something

## Requirements:
- Numpy `pip install numpy`(https://pypi.org/project/numpy/)
- OpenCV `pip install opencv-python` (https://pypi.org/project/opencv-python/)

## Usage:
```
barcode.py

Usage:
    barcode.py <inputfile> [outputfile] [--sps=<sps>]
    barcode.py -h | --help

Options:
    -h --help     Show this information
    [outputfile]  Set output filename
    --sps=<sps>   Samples Per Second - How many frames to sample from each second of video

Examples:
    barcode.py video.mp4 out.png --sps=4
```

## Example output:
`barcode.py video.mp4 example1.png`  
![It's something](https://github.com/Brakebusk/Video-Barcode/blob/master/example1.png)  

`barcode.py video.mp4 example2.png --sps=5`  
![It's something](https://github.com/Brakebusk/Video-Barcode/blob/master/example2.png)  
Original framerate is 25, which means we will sample every 5th frame (25/5=5)
