"""Generate the synthetic test images bundled with this repository.

Both images are produced entirely in code from a fixed seed: no photograph, no download, no third-party
asset. Re-running this script reproduces them byte-for-byte on the same OpenCV build, which is the point —
a reviewer can regenerate every pixel instead of taking provenance on trust.

    python tools/make_test_images.py
"""
import numpy as np
import cv2

W, H = 1408, 768


def scene_b():
    """A smooth, easy image: gradient sky, soft hills, one hard-edged structure and a label."""
    y, x = np.mgrid[0:H, 0:W].astype(np.float64)
    # sky: vertical gradient, light at the horizon
    t = np.clip(y / H, 0, 1)
    sky = np.dstack([215 - 70 * t, 228 - 55 * t, 245 - 25 * t])
    # sun: a smooth disc, low frequency
    d = np.sqrt((x - 0.78 * W) ** 2 + (y - 0.22 * H) ** 2)
    sun = np.clip(1.0 - d / (0.09 * W), 0, 1) ** 2
    sky += np.dstack([sun * 40, sun * 34, sun * 8])
    # hills: two cosine ridges, large smooth shapes
    h1 = 0.62 * H + 40 * np.cos(x / 190.0)
    h2 = 0.78 * H + 26 * np.cos(x / 120.0 + 1.1)
    img = sky.copy()
    img[y > h1] = np.array([110, 128, 96])
    img[y > h2] = np.array([74, 96, 66])
    # one hard-edged structure: crisp verticals and horizontals, the only high-frequency content
    x0, x1, y0, y1 = int(0.12 * W), int(0.30 * W), int(0.34 * H), int(0.62 * H)
    img[y0:y1, x0:x1] = np.array([196, 190, 178])
    img[y0:y0 + 8, x0:x1] = np.array([120, 116, 108])
    img[y0:y1, x0:x0 + 8] = np.array([120, 116, 108])
    for k in range(3):                                    # windows, evenly spaced
        wy = y0 + 40 + k * 70
        img[wy:wy + 34, x0 + 26:x0 + 76] = np.array([92, 104, 120])
        img[wy:wy + 34, x0 + 106:x0 + 156] = np.array([92, 104, 120])
    cv2.putText(img.astype(np.uint8), "DCT", (x0 + 18, y1 - 14), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                (40, 40, 40), 2, cv2.LINE_AA)
    return np.clip(img, 0, 255).astype(np.uint8)


def test_pattern(size=512):
    """A greyscale resolution chart: zone plate plus frequency wedges and a grey staircase."""
    y, x = np.mgrid[0:size, 0:size].astype(np.float64)
    cx = cy = size / 2.0
    r2 = (x - cx) ** 2 + (y - cy) ** 2
    plate = 127.5 + 127.5 * np.cos(np.pi * r2 / (size * 9.0))    # zone plate
    img = plate.copy()
    # vertical wedges: frequency rising left to right, three bands
    for band in range(3):
        y0 = int(0.02 * size) + band * int(0.10 * size)
        y1 = y0 + int(0.08 * size)
        f = np.linspace(2, 96, size)
        img[y0:y1, :] = 127.5 + 110 * np.sign(np.sin(2 * np.pi * f[None, :] * x[y0:y1, :] / size))
    # grey staircase along the bottom
    steps = np.repeat(np.linspace(0, 255, 9), size // 9 + 1)[:size]
    img[int(0.78 * size):int(0.88 * size), :] = steps[None, :]
    return np.clip(img, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    cv2.imwrite("Image/scene_b.jpg", scene_b(), [cv2.IMWRITE_JPEG_QUALITY, 95])
    cv2.imwrite("Image/test_pattern.png", test_pattern())
    print("wrote Image/scene_b.jpg and Image/test_pattern.png")
