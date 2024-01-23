import random
from enum import StrEnum
from time import sleep

import cv2
import pyautogui

from common import config
from common.break_functions import random_sleep
from shapely.geometry import Point

from common.config import ConsoleColors


def click_within_rectangles(loc, w, h, shrink_x=1, shrink_y=1, playarea=True, clicker='left',
                            fast=False):
    clicked_on_something = False
    # this should be made constant somewhere as I imagine cropx and cropy are based on something
    # these should probably be passed in also as it is based on inventory location
    if not playarea:
        cropx = 620
        cropy = 480
    else:
        cropx = 0
        cropy = 0
    for pt in zip(*loc[::-1]):
        if not pt:
            continue
        if config.image_debugging:
            debug_image = cv2.imread(config.image_debugging_location)
            cv2.rectangle(debug_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            cv2.imwrite(config.image_debugging_location, debug_image)

        x = random.randrange(shrink_x, w - shrink_x)
        y = random.randrange(shrink_y, h - shrink_y)

        if config.image_debugging:
            debug_image = cv2.imread(config.image_debugging_location)
            cv2.circle(debug_image, (pt[0] + x, pt[1] + y), radius=0, color=(0, 255, 255), thickness=4)
            cv2.imwrite(config.image_debugging_location, debug_image)

        coordinates = (pt[0] + x + cropx, pt[1] + y + cropy)
        random_duration_interaction(coordinates, Interactions.moveTo, clicker=clicker, fast=fast)
        random_duration_interaction(coordinates, Interactions.click, clicker=clicker, fast=fast)
        config.click_coordinates = coordinates
        clicked_on_something = True
    return clicked_on_something


def click_within_polygon(polygon, cropx=0, cropy=0):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    count = 0
    while len(points) < 1 and count < 10:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        x = int(pnt.x) + cropx
        y = int(pnt.y) + cropy
        if config.image_debugging:
            debug_image = cv2.imread(config.image_debugging_location)
            cv2.circle(debug_image, (x - cropx, y - cropy), radius=0, color=(0, 255, 255), thickness=1)
            cv2.imwrite(config.image_debugging_location, debug_image)
        count += 1
        if polygon.contains(pnt):
            points.append(pnt)
    # if we cant find a point within the polygon, return 0, 0
    # sometimes text will float above the polygon intersecting with it causing it to not be found
    # instead we break out of our search and return current point, it is usually close enough
    if count >= 10:
        print(ConsoleColors.FAIL + 'Could not find a point within the polygon')
        if not len(points) < 0:
            return 0, 0
    x = int(points[0].x) + cropx
    y = int(points[0].y) + cropy
    if config.image_debugging:
        debug_image = cv2.imread(config.image_debugging_location)
        cv2.circle(debug_image, (x - cropx, y - cropy), radius=0, color=(0, 255, 255), thickness=1)
        cv2.imwrite(config.image_debugging_location, debug_image)
    move_cursor_and_click((x, y), fast=True)
    return x, y


class Interactions(StrEnum):
    moveTo = 'moveTo',
    click = 'click'


def random_duration_interaction(coordinates, interaction, clicker='left', fast=False, instant=False):
    if instant:
        duration = 0.01
    elif fast:
        duration = random.uniform(0.01, 0.05)
    else:
        duration = random.uniform(0.1, 0.3)

    # switch instead?
    if interaction == Interactions.click:
        pyautogui.click(coordinates, duration=duration, button=clicker)
    elif interaction == Interactions.moveTo:
        pyautogui.moveTo(coordinates, duration=duration)


def click_options_menu_option(coordinates, option):
    if coordinates[1] > 780:
        raise ValueError('Coordinates are too low  and this doesnt account for squished options menu')
    random_duration_interaction(coordinates, Interactions.moveTo)
    random_sleep(0.5, 0.7)
    random_duration_interaction(coordinates, Interactions.click, clicker='right')
    random_sleep(0.2, 0.7)
    # 18 is the height of the options menu header, 15 is the height of each option
    menu_option_y = coordinates[1] + (18 + 15 * int(option) - random.randrange(3, 13))
    menu_option_x = coordinates[0] + random.randrange(-30, 30)
    menu_option_coordinates = (menu_option_x, menu_option_y)
    random_duration_interaction(menu_option_coordinates, Interactions.moveTo)
    random_sleep(0.2, 0.7)
    random_duration_interaction(menu_option_coordinates, Interactions.click)


def move_cursor_and_click(coordinates, clicker='left', fast=False, click_delay=0.1):
    random_duration_interaction(coordinates, Interactions.moveTo, clicker=clicker, fast=fast)
    if not fast:
        sleep(click_delay)
    random_duration_interaction(coordinates, Interactions.click, clicker=clicker, fast=fast)
