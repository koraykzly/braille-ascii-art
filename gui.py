"""
Helper script to view result in tkinter textbox.
Arguments are same as `braille.py` except --output option.
"""
import tkinter as tk
from tkinter import font
from braille import image_to_braille
import argparse
from os import path


def display_text_in_textbox(text):
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Text Display")

    text_widget = tk.Text(
        root, wrap=tk.NONE,
        font=font.Font(family="Consolas", size=5),
        bg='black', fg='white',
    )
    text_widget.insert("1.0", text)
    text_widget.config(state=tk.DISABLED)

    text_widget.pack(fill='both', expand=True)
    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description="Braille ASCII art generator.")
    parser.add_argument("image", help="Input file path.")
    parser.add_argument("-w", "--width",
                        help="Output width in characters. (Set -1 for original size)", type=int, default=300)
    parser.add_argument("-t", "--threshold",
                        help="Threshold value to convert binary image.", type=int, default=127)
    parser.add_argument("-s", "--swap", action="store_true",
                        help="Swap braille characters.", default=False)
    args = parser.parse_args()

    try:
        if not path.exists(args.image):
            raise FileNotFoundError()

        braille_art = image_to_braille(args.image, args.width, args.threshold, args.swap)
        display_text_in_textbox(braille_art)

    except FileNotFoundError:
        print("File not found: %s" % args.image)
    except Exception as e:
        print("Exception:", type(e), e)


if __name__ == "__main__":
    main()
