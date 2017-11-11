from __future__ import print_function
import argparse
import json
import logging
import numpy as np
import os
from PIL import Image
import sys


logger = logging.getLogger(__name__)


class Highlighter(object):
    """
    Methods for applying highlights to image from JSON description.
    """

    def __init__(self, image_filename, highlights_filename):
        self.image_filename = image_filename
        self.image = Image.open(image_filename).convert('RGB')

        with open(highlights_filename) as f:
            self.highlights = json.load(f)

        self.render_highlights()
        self.display_highlighted_image()
        self.save_highlighted_image()

    def render_highlights(self):
        """
        Apply highlighting to all described areas.
        """
        for highlight in self.highlights:
            box = self.compute_highlight_corners(highlight)
            region = self.image.crop(box)
            region.load()
            logger.debug("{}: {} - {} - {}".format(highlight['comment'],
                region.format, region.size, region.mode))
            color = self.compute_normalized_color(highlight)
            data2 = self.color_transform(region, color)
            img2 = Image.fromarray(data2, mode='RGB')
            self.image.paste(img2, box)

    def display_highlighted_image(self):
        """
        Display highlighted image.
        """
        self.image.load()
        self.image.show()

    def save_highlighted_image(self):
        """
        Save image.
        """
        self.image.save(self.compute_highlighted_filename())

    def compute_highlighted_filename(self):
        """
        Compute new filename.
        """
        (image_filename_base, image_filename_ext) = os.path.splitext(
                self.image_filename)
        image_filename_new = "{}_HIGHLIGHTED{}".format(
                image_filename_base, image_filename_ext)
        logger.debug("Writing highlighted image to: {}".format(
            image_filename_new))
        return image_filename_new

    def compute_highlight_corners(self, highlight):
        """
        Given x, y, width, height, compute upper left and lower right corners.
        """
        x1 = highlight['x']
        y1 = highlight['y']
        x2 = x1 + highlight['width']
        y2 = y1 + highlight['height']
        return (x1, y1, x2, y2)

    def compute_normalized_color(self, highlight):
        """
        Compute normalized colors from hex colors.
        """
        (r, g, b) = (0, 0, 0)
        if 'color' in highlight:
            color = highlight['color']
            # TODO: Support 3 character colors?
            if len(color) != 6:
                raise Exception('Requires hex RGB colors in format 112233.')
            r = int("0x{}".format("".join(list(color)[:2])), 16) / 255.0
            g = int("0x{}".format("".join(list(color)[2:4])), 16) / 255.0
            b = int("0x{}".format("".join(list(color)[4:6])), 16) / 255.0
        return [r, g, b]

    def normalize(self, im):
        """
        Normalize color values.
        """
        return -np.log(1/((1 + im)/257) - 1)

    def denormalize(self, im):
        """
        Restore color values.
        """
        return (1 + 1/(np.exp(-im) + 1) * 257).astype("uint8")

    def color_transform(self, region, color):
        """
        Apply color highlighting transform to image.
        """
        data = np.array(region)
        data_normed = self.normalize(data)
        data_xform = np.multiply(data_normed, np.array(color))
        data2 = self.denormalize(data_xform)
        return data2


class CustomArgumentParser(argparse.ArgumentParser): # pragma: no cover
    """
    Custom argparser.
    """
    def error(self, message):
        sys.stderr.write('error: {}\n'.format(message))
        self.print_help()
        sys.exit(2)

    def usage_message(self):
        """
        Print a message and exit.
        """
        sys.stderr.write("error: Missing required arguments.\n")
        self.print_help()
        sys.exit(3)


def main():
    """
    Parse command-line arguments. Initiate file processing.
    """
    parser = CustomArgumentParser()
    parser.add_argument("-i", "--image",
            help="Source file to highlight.")
    parser.add_argument("-d", "--highlights",
            help="JSON highlights description filename.")
    parser.add_argument("-v", "--verbose", help="Log level to DEBUG.",
            action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    error = False

    image_filename = args.image
    highlights_filename = args.highlights
    if not image_filename or not highlights_filename:
        error = True
        logger.error("Invalid arguments.")

    if error:
        logger.error("Exiting due to errors.")
        parser.usage_message()
        sys.exit(1)
    else:
        highlighter = Highlighter(image_filename, highlights_filename)


if __name__ == '__main__':  # pragma: no cover
    main()

