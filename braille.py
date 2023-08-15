""""
Braille ASCII Art Generator
"""
import cv2
import argparse
import numpy as np
from os import path


def intense(sample: np.ndarray):
    """
    Assumes given sample is binary image.
    (Contains either 255 or 0)
    """
    count_255 = np.sum(sample == 255)
    count_0 = sample.size - count_255
    return 1 if count_255 > count_0 else 0


def get_braille_char(code: str, swap: bool = False):
    empty, marked = "0", "1"
    braille_code = 0x00
    if swap:
        empty, marked = marked, empty
        braille_code = 0xFF

    _map = [0, 3, 1, 4, 2, 5, 6, 7]
    for index, mark in enumerate(code):
        if mark == marked:
            braille_code |= (2 ** _map[index])
        else:
            braille_code &= (~(2 ** _map[index]) & 0xFF)

    return chr(braille_code + 0x2800)


def to_matrix_code(data: np.ndarray, offset: int):
    """
    Represents the matrix
        0 1
        2 3
        4 5
        6 7

    like this:
        01234567
    """
    result = ""
    height, width = data.shape

    for i in range(0, height, offset):
        for j in range(0, width, offset):
            sub_pixel = data[i:i+offset, j:j+offset]
            intensed = intense(sub_pixel)
            result += str(intensed)
    return result


def read_image_grayscale(image_path: str):
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)


def to_binary_image(image: np.ndarray, threashold: int = 127):
    _, bw_image = cv2.threshold(image, threashold, 255, cv2.THRESH_BINARY)
    return bw_image


def resize(image: np.ndarray, new_width: int):
    if new_width < 0:
        new_width = 100
    new_width = 2 * new_width
    height, width = image.shape
    new_height = int(new_width * height / width)
    # print("%dx%d => %dx%d" % (width, height, new_width, new_height))
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)


def to_braille(image: np.ndarray, width: int, swap: bool = False) -> str:
    if not (width == -1):
        image = resize(image, width)

    height, width = image.shape
    result = ""
    OFFSET_X = 2
    OFFSET_Y = 2 * OFFSET_X

    for y in range(0, height, OFFSET_Y):
        for x in range(0, width, OFFSET_X):
            pixel = image[y:y+OFFSET_Y, x:x+OFFSET_X]
            braille_chr = to_matrix_code(pixel, int(OFFSET_X / 2 + 0.5))
            char = get_braille_char(braille_chr, swap)
            result += char
        result += "\n"
    return result


def image_to_braille(image_path, WIDTH=200, THRESHOLD=127, SWAP=False):
    """
    Image to braille art shortcut.
    """
    image = read_image_grayscale(image_path)
    bw_image = to_binary_image(image, THRESHOLD)
    braille_art = to_braille(bw_image, width=WIDTH, swap=SWAP)
    return braille_art


def main():
    parser = argparse.ArgumentParser(description="Braille ASCII art generator.")
    parser.add_argument("image", help="Input file path.")
    parser.add_argument("-w", "--width",
                        help="Output width in characters. (Set -1 for original size)", type=int, default=300)
    parser.add_argument("-t", "--threshold",
                        help="Threshold value to convert binary image.", type=int, default=127)
    parser.add_argument("-s", "--swap", action="store_true",
                        help="Swap braille characters.", default=False)
    parser.add_argument("-o", "--output",
                        help="Write the result to specified file.", default=None)
    args = parser.parse_args()

    try:
        if not path.exists(args.image):
            raise FileNotFoundError()

        braille_art = image_to_braille(args.image, args.width, args.threshold, args.swap)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as file:
                file.write(braille_art)
            return

        print(braille_art)
    except FileNotFoundError:
        print("File not found: %s" % args.image)
    except Exception as e:
        print("Exception:", type(e), e)


if __name__ == "__main__":
    main()
