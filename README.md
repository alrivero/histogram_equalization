# Histogram Equalizer: An Image Histogram Equalization Tool

## Environment
    Python 3.7

## Dependencies
    -   cv2

## Installation Guide
    -   cv2: `pip install opencv-python`

## Introduction
This is a simple image histogram equalization tool which relies on the cummulative distribution function (CDF) of each of an image's RGB channels to equalize an image's RGB color distribution histogram. Histogram equalization increaases the dynamic range of an image.

![Original Image](https://people.ucsc.edu/~alrivero/Other/in.jpg)
![Equalized Image](https://people.ucsc.edu/~alrivero/Other/eq.jpg)

Global and block histogram equalization is supported with adaptive histogram equalization planned.

## Usage
To use this tool, run 'equalize.py' and provide an image path following:
```bash
    python equalize.py -i <image_path>
```

A window displaying the globally-equalized image will be displayed. Optionally, the equalized image can be saved using the '-s' flag and block equalization can be enabled using the '-b' flag. When using block equalization, a block size integer must be provided.

```bash
    python equalize.py -i <image_path> -s <save_path> -b <block_size>
```

## Explanation of Code:

### Global Histogram Equalization
An image's histogram is equalized by computing the CDF of each R, G, and B channel's color distribution histogram. Once computed, the CDF is used as a look-up table which is applied to an image using OpenCV.

### Block Histogram Equlaization
Block histogram equalization is is identical to global histogram equalization. However, the image is partitioned into blocks where each block of pixels is treated as its own image. Each block is globally equalized.
  
## TODOs:
* Adaptive Histogram Equalization
* A GUI interface.

