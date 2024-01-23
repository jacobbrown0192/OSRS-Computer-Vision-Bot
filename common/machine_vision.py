import os
from enum import StrEnum

import cv2
import numpy
from PIL import ImageGrab, Image
from pytesseract import pytesseract
from shapely.geometry import Polygon

from common import config


def find_color_in_image_rectangle(image_full_location, color):
    image = cv2.imread(image_full_location)

    contours = get_color_contours_from_image(color, image)
    if len(contours) != 0:
        # find the biggest contour (largest_contour) by the area
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        if config.image_debugging:
            debug_image = cv2.imread(image_full_location)
            cv2.rectangle(debug_image, (x, y), (x + w, y + h), (0, 255, 255), 1)
            cv2.imwrite(image_full_location, debug_image)
        return x, y, w, h
    else:
        return None


def get_rectangle_from_contour(closest_contour, image_full_location, max_size):
    pass


def find_closest_color_in_image_rectangle(image_full_location, color, coordinates, max_size):
    image = cv2.imread(image_full_location)
    contours = get_color_contours_from_image(color, image)
    if len(contours) != 0:
        closest_contour = None
        distance_difference = 9999
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > max_size or h > max_size:
                continue
            distance = abs(x - coordinates[0]) + abs(y - coordinates[1])
            if distance < distance_difference:
                closest_contour = contour
                distance_difference = distance
                if distance < 2:
                    break
        if closest_contour is not None:
            return cv2.boundingRect(closest_contour)
        else:
            return None
    else:
        return None


def find_closest_color_in_image_precise(image_full_location, color, coordinates):
    image = cv2.imread(image_full_location)
    contours = get_color_contours_from_image(color, image)
    if len(contours) != 0:
        closest_contour = None
        distance_difference = 9999
        for contour in contours:
            if len(contour) > 4:
                x, y, w, h = cv2.boundingRect(contour)
                if w < 3 or h < 3:
                    continue
                distance = abs(x - coordinates[0]) + abs(y - coordinates[1])
                if distance < distance_difference:
                    closest_contour = contour
                    distance_difference = distance
                    if distance < 2:
                        break
        return get_polygon_from_contour(closest_contour, image_full_location)
    else:
        return None


# TODO need a check for a 0d array
def get_polygon_from_contour(contour, image_full_location):
    if contour is not None:
        color_polygon = Polygon(numpy.squeeze(contour))
        if config.image_debugging:
            debug_image = cv2.imread(image_full_location)
            cv2.drawContours(debug_image, contour, -1, (0, 255, 0), 1)
            cv2.imwrite(image_full_location, debug_image)
        return color_polygon
    else:
        return None


def get_color_contours_from_image(color, image):
    (lower, upper) = COLOR_BOUNDARIES[color]
    lower = numpy.array(lower, dtype="uint8")
    upper = numpy.array(upper, dtype="uint8")
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    thresh_used, threshold_image = cv2.threshold(mask, 40, 255, 0)
    # cv2.imwrite('images/temp.png', threshold_image)
    # can probably use CHAIN_APPROX_SIMPLE instead of CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours


# I think left top right bottom are the wrong words
# should probably return screenshot location or just the screen shot in general
def screen_shot_save_images(min_x=0, min_y=0, max_x=0, max_y=0, image_name='screenshot.png'):
    if min_x != 0 or min_y != 0 or max_x != 0 or max_y != 0:
        screenshot = ImageGrab.grab(bbox=(min_x, min_y, max_x, max_y))
    else:
        screenshot = ImageGrab.grab(bbox=(
            config.window_x, config.window_y, config.window_x + config.window_w, config.window_y + config.window_h))
    screenshot.save('images/' + image_name, 'png')


def skilling_screenshot_and_resize(image_name='skilling_text.png'):
    # cordinates of skilling area related to the client size
    left = 40
    top = 49
    right = 105
    bottom = 69
    screen_shot_save_images(left, top, right, bottom, image_name='skilling_original.png')
    skilling_screenshot = Image.open('./images/skilling_original.png')
    # saves new cropped image
    width, height = skilling_screenshot.size
    new_size = (width * 4, height * 4)
    skilling_screenshot_resized = skilling_screenshot.resize(new_size)
    skilling_screenshot_resized.save('images/' + image_name)


def change_brown_black(image_name='skilling_text.png'):
    image = cv2.imread("images/" + image_name)

    # Define lower and uppper limits of what we call "brown"
    brown_lo = numpy.array([0, 0, 0])
    brown_hi = numpy.array([60, 80, 85])

    # Mask image to only select browns
    mask = cv2.inRange(image, brown_lo, brown_hi)

    # Change image to red where we found brown
    image[mask > 0] = (0, 0, 0)
    cv2.imwrite("images/" + image_name, image)


def image_to_text(preprocess, image='skilling_text.png', parse_config='--psm 7'):
    skilling_screenshot_and_resize(image)
    change_brown_black(image)
    # construct the argument parse and parse the arguments
    image = cv2.imread('images/' + image)
    image = cv2.bitwise_not(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # TODO create enum of these
    # check to see if we should apply thresholding to preprocess the image
    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove noise
    if preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    if preprocess == 'adaptive':
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    with Image.open(filename) as im:
        text = pytesseract.image_to_string(im, config=parse_config)
    os.remove(filename)
    return text


# Improve this using some of the other implementations in functions.py
def find_image_in_screenshot(image_name, screenshot='screenshot.png', threshold=0.7):
    img_rgb = cv2.imread('images/' + screenshot)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # TODO have a list of defined objects somewhere Move objects to a different folder
    template = cv2.imread('images/' + image_name, 0)
    template_w, template_h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = numpy.where(res >= threshold)
    return loc, template_w, template_h, img_rgb


def image_count(image_name, threshold=0.8, left=0, top=0, right=0, bottom=0, debug_image=False):
    counter = 0
    screen_shot_save_images(left, top, right, bottom, image_name='screenshot.png')
    loc, template_w, template_h, img_rgb = find_image_in_screenshot(image_name, threshold=threshold)
    for pt in zip(*loc[::-1]):
        if debug_image:
            cv2.rectangle(img_rgb, pt, (pt[0] + template_w, pt[1] + template_h), (0, 0, 255), 2)
        counter += 1
    return counter


class Colors(StrEnum):
    red = 'red',
    green = 'green',
    blue = 'blue',
    mining_blue = 'mining_blue',
    amber = 'amber',
    pickup = 'pickup',
    attack_blue = 'attack_blue'
    options_menu = 'options_menu'


COLOR_BOUNDARIES = {
    Colors.red: ([0, 0, 180], [80, 80, 255]),
    Colors.green: ([0, 180, 0], [80, 255, 80]),
    Colors.mining_blue: ([230, 0, 0], [255, 25, 25]),
    Colors.blue: ([255, 0, 0], [255, 0, 0]),
    Colors.amber: ([0, 160, 160], [80, 255, 255]),
    Colors.pickup: ([200, 0, 100], [255, 30, 190]),
    Colors.attack_blue: ([250, 250, 0], [255, 255, 5]),
    Colors.options_menu: ([71, 84, 93], [71, 84, 93])
}
