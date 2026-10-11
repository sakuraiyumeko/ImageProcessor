from PIL import Image
from pathlib import Path

BASE_PATH = Path(r"E:\.0a_111111\Videos and Photos\Photos")
LOCAL_PATH = Path(__file__).resolve().parent

mapping = {
    0: "R",
    1: "G",
    2: "B",
}

IMG_NAME_1 = "example1.jpg"
IMG_NAME_2 = "example2.jpg"


def loadimg(name):
    img = Image.open(LOCAL_PATH / name)
    img = img.convert("RGB")
    size = img.size
    width, height = size
    pixels = list(img.get_flattened_data())
    new_pixels = [[0, 0, 0] for _ in pixels]
    return [img, size, pixels, new_pixels]


def img_split_rgb(name=IMG_NAME_1):
    img, size, pixels, new_pixels = loadimg(name)
    for c in range(3):
        new_pixels = [
            tuple(pixel[c] if i == c else 0 for i in range(3)) for pixel in pixels
        ]
        new_img = Image.new(img.mode, (size[0], size[1]))
        new_img.putdata(new_pixels)
        new_img.save(LOCAL_PATH / f"{mapping[c]}-{name.split(".")[0]}.png")


def img_combine(name1=IMG_NAME_1, name2=IMG_NAME_2, mode="avg", mod_value=256):
    img1, size1, pixels1, new_pixels = loadimg(name1)
    img2 = loadimg(name2)
    size2, pixels2 = img2[1], img2[2]
    if size1 != size2:
        print(f"{name1} and {name2} have different size. That might be cause some question.")
    if mode == "avg":
        new_pixels = [
            tuple(min((a + b) / 2, 255) for a, b in zip(pixel1, pixel2))
            for pixel1, pixel2 in zip(pixels1, pixels2)
        ]
    elif mode == "mod":
        new_pixels = [
            tuple((a + b) % mod_value for a, b in zip(pixel1, pixel2))
            for pixel1, pixel2 in zip(pixels1, pixels2)
        ]

    new_img = Image.new(img1.mode, (size1[0], size1[1]))
    new_img.putdata(new_pixels)
    new_img.save(
        LOCAL_PATH / f"combined-{name1.split(".")[0]}-{name2.split(".")[0]}.png"
    )


def img_invert(name=IMG_NAME_1):
    img, size, pixels, new_pixels = loadimg(name)
    new_pixels = [tuple(255 - pixel[c] for c in range(3)) for pixel in pixels]
    new_img = Image.new(img.mode, (size[0], size[1]))
    new_img.putdata(new_pixels)
    new_img.save(LOCAL_PATH / f"inverted-{name.split(".")[0]}.png")
