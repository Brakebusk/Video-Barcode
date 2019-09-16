# Video-Barcode
It's something

## Requirements:
- Numpy `pip install numpy`(https://pypi.org/project/numpy/)
- OpenCV `pip install opencv-python` (https://pypi.org/project/opencv-python/)

## Usage:
```
barcode.py

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
    barcode.py video.mp4 out.png --ar=3:2
```

## Example output:
`barcode.py alien.mp4 alien.png --ar=21:9 --ignore=164 --autocrop`  
![Alien Theatrical cut](https://github.com/Brakebusk/Video-Barcode/blob/master/Examples/alien.png)  

`barcode.py atlantis.mp4 atlantis.png --ar=21:9 --ignore=375`  
![Atlantis The Lost Empire](https://github.com/Brakebusk/Video-Barcode/blob/master/Examples/atlantis.png)  
