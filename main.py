from PIL import Image
from pathlib import Path
import numpy as np
import time

BASE_PATH = Path(r"E:\.0a_111111\Videos and Photos\Photos")
LOCAL_PATH = Path(__file__).resolve().parent
SAVE_PATH = LOCAL_PATH / "Output"

mapping = {
    0: "R",
    1: "G",
    2: "B",
}


IMG_NAME_1 = "example1.png"
IMG_NAME_2 = "example2.png"

def loadimg(name):
    img = Image.open(LOCAL_PATH / name)
    img = img.convert("RGB")
    size = img.size
    pixels = list(img.get_flattened_data())
    return [img, size, pixels]


def saveimg(img, save_name, size, new_pixels):
    new_img = Image.new(img.mode, (size[0], size[1]))
    new_img.putdata(new_pixels)
    new_img.save(SAVE_PATH / save_name)


def img_split_rgb(name=IMG_NAME_1):
    suffix = int(time.time_ns())
    img, size, pixels = loadimg(name)
    for c in range(3):
        new_pixels = [
            tuple(pixel[c] if i == c else 0 for i in range(3)) for pixel in pixels
        ]
        saveimg(img, f"{mapping[c]}-{Path(name).stem}-{suffix}.png", size, new_pixels)


def img_combine(
    name1=IMG_NAME_1, name2=IMG_NAME_2, mode="avg", mod_value=256, weight=0.5
):
    suffix = int(time.time())
    img1, size1, pixels1 = loadimg(name1)
    img2 = loadimg(name2)
    size2, pixels2 = img2[1], img2[2]
    if size1 != size2:
        print(
            f"{name1} and {name2} have different size. That might be cause some question."
        )
    if mode == "avg":
        new_pixels = [
            tuple(
                min((weight * a + (1 - weight) * b), 255)
                for a, b in zip(pixel1, pixel2)
            )
            for pixel1, pixel2 in zip(pixels1, pixels2)
        ]
    elif mode == "mod":
        new_pixels = [
            tuple((a + b) % mod_value for a, b in zip(pixel1, pixel2))
            for pixel1, pixel2 in zip(pixels1, pixels2)
        ]

    saveimg(
        img1, f"combined-{Path(name1).stem}-{Path(name2).stem}-{suffix}.png", size1, new_pixels
    )


def img_invert(name=IMG_NAME_1, isR=1, isG=1, isB=1, threshold=0):
    suffix = int(time.time())
    img, size, pixels = loadimg(name)
    new_pixels = [
        tuple(
            pixel[c] ^ (255 * enabled) if pixel[c] >= 255 * threshold else pixel[c]
            for c, enabled in enumerate((isR, isG, isB))
        )
        for pixel in pixels
    ]
    saveimg(img, f"inverted-{Path(name).stem}-{suffix}.png", size, new_pixels)


def img_bit_depth(name=IMG_NAME_1, depth=4, raw_depth=8):
    suffix = int(time.time())
    img, size, pixels = loadimg(name)
    levels = 2**depth - 1
    raw_levels = 2**raw_depth - 1
    new_pixels = [
        tuple(
            round(round(channel / raw_levels * levels) / levels * raw_levels)
            for channel in pixel
        )
        for pixel in pixels
    ]
    saveimg(img, f"{depth}bit-{Path(name).stem}-{suffix}.png", size, new_pixels)


def img_binarization():
    suffix = int(time.time())
    pass

    
for i in range(1,11):
    img_invert(threshold=i/10)