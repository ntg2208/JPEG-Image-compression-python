# Image compression and the Discrete Cosine Transform
Imlementation of lossy image compression using DCT method (JPEG standard), base on **_Ken Cabeen_** and **_Peter Gent_** [document](https://github.com/ntg2208/JPEG-Image-compresion-python-example/blob/master/Document/dct.pdf).

## Usage

```bash
python DCT.py <input_file> <level_of_compression>
python DCT.py Image/car1.jpg 50 
```

## Introduction
 - As our use of and reliance on computers continues to grow, so does the need for efficient ways of storing large amounts of data.
 - Two kind of compression alorithm: lossless and lossy image compression.
 - JPEG is an lossy image compression using Discrete Cosine Transform to separate into parts of different frequencies. 
 - Apply a process called quantization, where the less important information are discarded -> reconstructed image contain distortion but size of image are reduced.

 ## Overview the process
 
1. The image broken into 8x8 blocks of pixels.
2. Working from left to right, top to bottom, the DCT is applied to each block.
3. Each block is compressed through quantization.
4. The array of compressed blocks that constitute the image is stored/ transmitted in a less amount of size.
4. When desired, the image is reconstructed through decompression, using Inverse Discrete Cosine Transform (IDCT).

## DCT Equation

![alt text][equation]

[equation]: https://github.com/ntg2208/JPEG-Image-compresion-python-example/blob/master/Document/DCT_eq.png


Using opencv to compress/decompress image base on Discrete Cosine Transform

For more detail about JPEG compression, read file dct.pdf

