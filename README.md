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
![It's something](https://github.com/Brakebusk/Video-Barcode/blob/master/output.png)
