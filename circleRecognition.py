import sys
import cv2 as cv
import numpy as np
import os
import math
import constants


# https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html
def makeCircles(src):
    # gray = cv.medianBlur(src, 17)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    col = gray.shape[1]
    gray = cv.GaussianBlur(gray, (5, 5), 1.5)

    circles = cv.HoughCircles(
        gray,
        cv.HOUGH_GRADIENT,
        1.2,
        col // 18,
        param1=100,
        param2=50,
        minRadius=col // 50,
        maxRadius=col // 5,
    )

    return None if circles is None else circles[0, :]


def findPointsOnCircle(x, y, rad, n, maxX, maxY):
    t = 0
    result = []
    step = math.pi * 2 / n
    rad *= 1.1

    while t < math.pi * 2:
        dx = math.cos(t) * rad
        dy = math.sin(t) * rad
        xlist = [0, x + dx, maxX]
        ylist = [0, y + dy, maxY]
        xlist.sort()
        ylist.sort()
        result.append((int(xlist[1]), int(ylist[1])))
        t += step

    return result


def openFile(filename, directory):
    f = os.path.join(directory, filename)
    src = None
    if os.path.isfile(f):
        src = cv.imread(cv.samples.findFile(f), cv.IMREAD_COLOR)
    if src is None:
        print("Error opening image!")
        print("Usage: hough_circle.py [image_name -- default " + f + "] \n")
        return -1
    return src


def labelCircle(img):
    cv.imshow(constants.DISPLAY_WINDOW_NAME, img)
    print(
        "Classify image: [0='1', 1='10', 2='100', 3='5', 4='50', 5='500', enter=<skip>]"
    )
    # c = int(input())
    key = cv.waitKey(0)
    label = -1
    while key != 13:
        classes = [1, 10, 100, 5, 50, 500]
        label = classes[key - 48]
        print("Selected: %s" % (label))
        print("Press <enter> to finalize")
        key = cv.waitKey(0)
        print()
    return label


def cleanCircles(circles):
    i = 0
    while i < len(circles):
        current = circles[i]
        j = i + 1

        while j < len(circles):
            other = circles[j]

            dx = int(other[0]) - current[0]
            dy = int(other[1]) - current[1]
            distance = pow(dx, 2) + pow(dy, 2)
            if distance < pow(
                max(other[2], current[2]), 2
            ) * constants.OVERLAP_THREASHOLD and other[2] in range(
                int(current[2] * 0.7), int(current[2] * 1.3)
            ):
                if current[2] < other[2]:
                    circles = np.delete(circles, i, 0)
                    i -= 1
                    break
                else:
                    circles = np.delete(circles, j, 0)
                    j -= 1
            j += 1
        i += 1
    return circles


def findCircles():
    if not os.path.exists(constants.LABEL_DIRECTORY):
        os.mkdir(constants.LABEL_DIRECTORY)
    if not os.path.exists(constants.LABELED_IMAGES_DIRECTORY):
        os.mkdir(constants.LABELED_IMAGES_DIRECTORY)

    directory = constants.COMPRESS_DIRECTORY
    for filename in os.listdir(directory):
        # original = openFile(filename, constants.TRAINING_DATA_DIRECTORY)
        # cv.imshow("original", original)
        # cv.waitKey(0)
        src = openFile(filename, directory)
        final = src.copy()

        rows = src.shape[1]
        cols = src.shape[0]

        circles = makeCircles(src)
        if circles is None:
            continue

        circles = np.uint16(np.around(circles))
        # circles = cleanCircles(circles)

        imageLabel = []
        for i in circles:
            print(i)
            imgCopy = src.copy()
            center = (i[0], i[1])
            cv.circle(imgCopy, center, 1, (0, 100, 100), 3)
            cv.circle(final, center, 1, (0, 100, 100), 3)

            # circle points
            points = findPointsOnCircle(
                i[0], i[1], i[2], 12, imgCopy.shape[1], imgCopy.shape[0]
            )
            for p in points:
                cv.circle(imgCopy, p, 1, (255, 0, 255), 3)
                cv.circle(final, p, 1, (255, 0, 255), 3)

            label = labelCircle(imgCopy)

            if not label == -1:
                circleLabel = (
                    str(label)
                    + " "
                    + " ".join(
                        [str(p[0] / rows) + " " + str(p[1] / cols) for p in points]
                    )
                )

                imageLabel.append(circleLabel)

        data = "\n".join(imageLabel)

        labelfilename = constants.LABEL_DIRECTORY + "/" + filename[:-4] + ".txt"
        f = open(labelfilename, "w")
        f.write(data)
        f.close()

        cv.imwrite(
            constants.LABELED_IMAGES_DIRECTORY + "/transformed" + filename, final
        )

    return 0
