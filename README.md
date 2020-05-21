# Image compression and the Discrete Cosine Transform
Imlementation of lossy image compression using DCT method (JPEG standard), base on **_Ken Cabeen_** and **_Peter Gent_** document.

## Usage

```bash
python DCT.py Image/car1.jpg 50 
```

## Introduction
 - As our use of and reliance on computers continues to grow, so does the need for efficient ways of storing large amounts of data.
 - Two kind of compression alorithm: lossless and lossy image compression.
 - JPEG is an lossy image compression using Discrete Cosine Transform to separate into parts of different frequencies. Then apply a process called quantization, where the less important information are discarded -> reconstructed image contain distortion but size of image are reduced.

 ## Overview the process
 




Using opencv to compress/decompress image base on Discrete Cosine Transform

For more detail about JPEG compression, read file dct.pdf

