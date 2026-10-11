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
    pixels = list(img.get_flattened_data())
    new_pixels = [[0, 0, 0] for _ in pixels]
    return [img, size, pixels, new_pixels]

def saveimg(img,save_name,size,new_pixels):
    new_img = Image.new(img.mode, (size[0], size[1]))
    new_img.putdata(new_pixels)
    new_img.save(LOCAL_PATH / save_name)

def img_split_rgb(name=IMG_NAME_1):
    img, size, pixels, new_pixels = loadimg(name)
    for c in range(3):
        new_pixels = [
            tuple(pixel[c] if i == c else 0 for i in range(3)) for pixel in pixels
        ]
        saveimg(img,f"{mapping[c]}-{Path(name).stem}.png",size,new_pixels)


def img_combine(
    name1=IMG_NAME_1, name2=IMG_NAME_2, mode="avg", mod_value=256, weight=0.5
):
    img1, size1, pixels1, new_pixels = loadimg(name1)
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
        
    saveimg(img1,f"combined-{Path(name1).stem}-{Path(name2).stem}.png",size1,new_pixels)


def img_invert(name=IMG_NAME_1, isR=1, isG=1, isB=1):
    img, size, pixels, new_pixels = loadimg(name)
    new_pixels = [
        tuple(pixel[c] ^ (255 * enabled) for c, enabled in enumerate((isR, isG, isB)))
        for pixel in pixels
    ]
    saveimg(img,f"inverted-{name.split(".")[0]}.png",size,new_pixels)


def img_bit_depth(name=IMG_NAME_1, depth=4, raw_depth=8):
    img, size, pixels, new_pixels = loadimg(name)
    new_pixels = [
        tuple((pixel[c]/raw_depth)*(2**depth-1) for c in range(3)) for pixel in pixels
    ]
    saveimg(img,f"{depth}bit-{name.split(".")[0]}.png",size,new_pixels)