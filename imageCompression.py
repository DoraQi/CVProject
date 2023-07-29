# importing the required modules
import os
from PIL import Image, ImageEnhance
import imghdr
import constants


# Function to compress the image
def compressImage(image_file, original_file):
    # accessing the image file
    filepath = os.path.join(os.getcwd(), image_file)

    # opening the file
    image = Image.open(filepath)

    # Calculating the width and height of the original photo
    width, height = image.size
    # calculating the aspect ratio of the image
    aspectratio = width / height

    # Calculating the new height of the compressed image
    newheight = constants.MAX_IMG_WIDTH / aspectratio

    # Resizing the original image
    image = image.resize((constants.MAX_IMG_WIDTH, round(newheight)))
    # image = image.convert("L")

    enhancer = ImageEnhance.Contrast(image)

    factor = 1.6
    image = enhancer.enhance(factor)

    # Saving the image
    filename = (
        constants.COMPRESS_DIRECTORY
        # + "/compressed"
        + "/"
        + original_file
    )
    image.save(filename, optimize=True, quality=85)
    return


def compressImages(directory):
    if not os.path.exists(constants.COMPRESS_DIRECTORY):
        os.mkdir(constants.COMPRESS_DIRECTORY)
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            compressImage(f, filename)
