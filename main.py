import circleRecognition
import imageCompression
import sys
import constants
import shutil

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        shutil.rmtree(constants.LABELED_IMAGES_DIRECTORY)
        shutil.rmtree(constants.COMPRESS_DIRECTORY)
        shutil.rmtree(constants.LABEL_DIRECTORY)
    else:
        if len(sys.argv) > 1 and sys.argv[1] == "1":
            # imageCompression.compressImages(constants.TRAINING_DATA_DIRECTORY)
            imageCompression.compressImages("smol")
        circleRecognition.findCircles()
