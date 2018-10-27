import cv2
import numpy as np
import pyautogui
import random
import time


def region_grabber(region):
    """
    grabs a region (topx, topy, bottomx, bottomy)
    to the tuple (topx, topy, width, height)
    
    :param region: A tuple containing the 4 coordinates of the region to capture
    :return: A PIL image of the area selected.
    """
    x1 = region[0]
    y1 = region[1]
    width = region[2] - x1
    height = region[3] - y1

    return pyautogui.screenshot(region=(x1, y1, width, height))


def imagesearcharea(image, x1, y1, x2, y2, precision=0.8, im=None):
    """
    Searches for an image within an area

    :param image: Path to the image file (see opencv imread for supported types)
    :param x1: Top left x value
    :param y1: Top left y value
    :param x2: Bottom right x value
    :param y2: Bottom right y value
    :param precision : The higher, the lesser tolerant and fewer false positives are found default is 0.8
    :param im: A PIL image, useful if you intend to search the same unchanging region for several elements
    :return: The top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not
    """
    if im is None:
        im = region_grabber(region=(x1, y1, x2, y2))

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


def click_image(image, pos, action, timestamp, offset=5):
    """
    click on the center of an image with a bit of random, eg: if an image is 100*100 with an offset of 5 it may click
    at 52,50 the first time and then 55,53 etc. This is useful to avoid anti-bot monitoring while staying precise.
    this function doesn't search for the image, it's only meant for easy clicking on the images.

    :param image: Path to the image file (see opencv imread for supported types)
    :param pos: Array containing the position of the top left corner of the image [x,y]
    :param action: Button of the mouse to activate : "left" "right" "middle", see pyautogui.click documentation for more info
    :param timestamp: Time taken for the mouse to move from where it was to the new position
    :param offset: The offset to which the pointer can reach, default offset is 5
    """
    img = cv2.imread(image)
    height, width, channels = img.shape
    pyautogui.moveTo(pos[0] + r(width / 2, offset), pos[1] + r(height / 2, offset),
                     timestamp)
    pyautogui.click(button=action)


def imagesearch(image, precision=0.8):
    """
    Searches for an image on the screen

    :param image: Path to the image file (see opencv imread for supported types)
    :param precision: The higher, the lesser tolerant and fewer false positives are found default is 0.8
    :return: The top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not
    """
    im = pyautogui.screenshot()
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]  # TODO: Remove?

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


def imagesearch_loop(image, timesample, precision=0.8):
    """
    Searches for an image on screen continuously until it's found.

    :param image: Path to the image file (see opencv imread for supported types)
    :param timesample: Waiting time after failing to find the image
    :param precision: The higher, the lesser tolerant and fewer false positives are found default is 0.8
    :return: The top left corner coordinates of the element if found as an array [x,y]
    """
    pos = imagesearch(image, precision)
    while pos[0] == -1:
        print(image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
    return pos


def imagesearch_loop2(image, image2, timesample, precision=0.8):
    """
    Searches for two images on screen continuously until it's found. It will first search for 'image', if it is not
    found it will wait for 'timesample' millis and after this it will start searching for 'image2', this loop will
    continue afterward.

    :param image: Path to the image file (see opencv imread for supported types)
    :param timesample: Waiting time after failing to find the image
    :param precision: The higher, the lesser tolerant and fewer false positives are found default is 0.8
    :return: The top left corner coordinates of the element if found as an array [x,y]
    """
    pos = imagesearch(image, precision)
    twist = True
    while pos[0] == -1:
        time.sleep(timesample)
        if twist:
            print(image + " not found, waiting")
            pos = imagesearch(image, precision)
            twist = False
        else:
            print(image2 + " not found, waiting")
            pos = imagesearch(image2, precision)
            twist = True
    return pos


def imagesearch_region_loop(image, timesample, x1, y1, x2, y2, precision=0.8):
    """
    Searches for an image on a region of the screen continuously until it's found.

    :param image: Path to the image file (see opencv imread for supported types)
    :param timesample: Waiting time after failing to find the image
    :param x1: Top left x value
    :param y1: Top left y value
    :param x2: Bottom right x value
    :param y2: Bottom right y value
    :param precision: The higher, the lesser tolerant and fewer false positives are found default is 0.8
    :return: The top left corner coordinates of the element as an array [x,y]
    """
    pos = imagesearcharea(image, x1, y1, x2, y2, precision)

    while pos[0] == -1:
        time.sleep(timesample)
        pos = imagesearcharea(image, x1, y1, x2, y2, precision)
    return pos


def r(num, rand):
    return num + rand * random.random()
