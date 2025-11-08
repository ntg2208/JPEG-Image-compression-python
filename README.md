# Image Compression using Discrete Cosine Transform

Implementation of lossy image compression using the DCT method (JPEG standard), based on **_Ken Cabeen_** and **_Peter Gent_** [document](https://github.com/ntg2208/JPEG-Image-compresion-python-example/blob/master/Document/dct.pdf).

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [DCT Equation](#dct-equation)
- [Output Files](#output-files)
- [Code Review Notes](#code-review-notes)
- [References](#references)

## Introduction

As our use of and reliance on computers continues to grow, so does the need for efficient ways of storing large amounts of data. This project implements JPEG-style lossy image compression using the Discrete Cosine Transform (DCT).

**Key Concepts:**
- Two kinds of compression algorithms: **lossless** and **lossy** image compression
- JPEG uses lossy compression with DCT to separate images into parts of different frequencies
- Through quantization, less important frequency information is discarded
- The reconstructed image contains some distortion, but file size is significantly reduced

## Requirements

- Python 3.x
- NumPy
- OpenCV (cv2)
- Matplotlib

## Installation

```bash
# Install required packages
pip install numpy opencv-python matplotlib

# Or using requirements.txt (recommended)
pip install -r requirements.txt
```

**Note:** Create a `requirements.txt` file with:
```
numpy>=1.19.0
opencv-python>=4.5.0
matplotlib>=3.3.0
```

## Usage

### Basic Usage

```bash
python DCT.py <input_file> <compression_level>
```

### Examples

```bash
# Medium compression (quality 50)
python DCT.py Image/car1.jpg 50

# High quality (low compression)
python DCT.py Image/car2.jpg 90

# Low quality (high compression)
python DCT.py Image/cameraman.tif 10
```

**Compression Level Guide:**
- `1-30`: High compression, lower quality
- `30-70`: Moderate compression, good balance
- `70-100`: Low compression, high quality (closer to original)

**Important:** The input image dimensions should be divisible by 8 for proper block processing. The script does not currently handle padding for non-conforming dimensions.

## How It Works

### Overview of the Process

1. **Block Division:** The image is broken into 8×8 blocks of pixels
2. **DCT Application:** Working from left to right, top to bottom, the DCT is applied to each block
3. **Quantization:** Each block is compressed through quantization (discarding high-frequency components)
4. **Storage:** The array of compressed blocks is stored with reduced size
5. **Decompression:** When desired, the image is reconstructed using Inverse DCT (IDCT)

### Processing Steps (Technical)

1. Convert image to RGB channels and subtract 128 (center around zero)
2. Apply DCT to each 8×8 block using the DCT coefficient matrix
3. Quantize DCT coefficients using JPEG standard quantization tables
4. For decompression: multiply by quantization matrix and apply IDCT
5. Add 128 back and merge channels to reconstruct the image

## DCT Equation

The Discrete Cosine Transform coefficient matrix is computed as:

![DCT Equation][equation]

[equation]: https://github.com/ntg2208/JPEG-Image-compresion-python-example/blob/master/Document/DCT_eq.png

Where the DCT coefficient matrix T is defined as:
- T[0,j] = 1/√8 for all j
- T[i,j] = √(2/8) × cos((2j+1)iπ/16) for i > 0

## Output Files

The script generates three output files in the current directory:

1. **`DCT.jpg`** - Visualization of DCT coefficients
2. **`After_Quantiz.jpg`** - Quantized DCT coefficients
3. **`Decompressed.jpg`** - Final reconstructed image

### Performance Metrics

The script outputs:
- **Compression/Decompression Time** - Processing time for each operation
- **RMS Error** - Root Mean Square error between original and decompressed image
- **SNR** - Signal-to-Noise Ratio (higher is better)

## Code Review Notes

### Known Issues

1. **DCT_compress.py** is incomplete:
   - Missing `quantization_level()` function definition
   - Import statements at the bottom (should be at top)
   - Contains Jupyter notebook artifacts

2. **Limited error handling:**
   - No validation for file existence
   - No check if image dimensions are divisible by 8
   - No exception handling for file I/O operations

3. **Hardcoded outputs:**
   - Output files are always written to the current directory
   - Output filenames cannot be customized

### Recommendations for Improvement

- Add input validation (file existence, dimensions)
- Add error handling with try-except blocks
- Make output paths configurable via command-line arguments
- Add function docstrings
- Fix DCT_compress.py or remove if not needed
- Add padding for images not divisible by 8

## References

For more details about JPEG compression and DCT:
- See `Document/dct.pdf` in this repository
- [DCT Equation Image](https://github.com/ntg2208/JPEG-Image-compresion-python-example/blob/master/Document/DCT_eq.png)
- Ken Cabeen and Peter Gent's original documentation

## License

See repository for license information.
