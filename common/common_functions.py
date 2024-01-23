import random
import time
from threading import Thread

import cv2
import pyautogui

from common import config
from common.client_interaction import click_within_rectangles, click_within_polygon, move_cursor_and_click
from common.machine_vision import find_color_in_image_rectangle, screen_shot_save_images, find_image_in_screenshot, \
    image_count, find_closest_color_in_image_precise, Colors, find_closest_color_in_image_rectangle


def get_current_time():
    start_time = time.time()
    return start_time


# should make a generic progress function
# mining progress message defined in miner
# def print_mining_progress(current_time, start_time, end_time, click_coordinates, status, ore_count, gem_count,
#                           clue_count, actions):


def get_inventory(key):
    return config.inventory.get(key) or 0


# Ideally this would be on an event loop instead of looping itself
def timer_countdown_loop_mining(progress_print_function):
    final = round((60 * 60 * config.run_duration_hours) / 1)

    for i in range(final):
        progress_print_function()
        time.sleep(1)


# change this to take in a printing progress function
# This thread acts as an event loop
def start_timer_countdown_loop(progress_print_function):
    t1 = Thread(target=timer_countdown_loop_mining, args=(progress_print_function,))
    t1.start()


def break_message(time_to_next_break):
    print("Will break in: %.2f" % (time_to_next_break / 60) + " minutes")


def click_within_rectangle(x, y, w, h, cropx=0, cropy=0, x_shrink=5, y_shrink=5):
    # need to account for shrink being too large for rectangle
    x = random.randrange(x + x_shrink, x + max(w - x_shrink, 6)) + cropx  # 950,960
    y = random.randrange(y + y_shrink, y + max(h - y_shrink, 6)) + cropy  # 490,500
    if config.image_debugging:
        debug_image = cv2.imread(config.image_debugging_location)
        cv2.circle(debug_image, (x - cropx, y - cropy), radius=0, color=(0, 255, 255), thickness=4)
        cv2.imwrite(config.image_debugging_location, debug_image)
    random_move_duration = random.uniform(0.1, 0.3)
    pyautogui.moveTo(x, y, duration=random_move_duration)
    random_click_duration = random.uniform(0.07, 0.11)
    pyautogui.click(duration=random_click_duration)
    return x, y


def find_color_and_click_rectangle(image_full_location, color, cropx, cropy, shrink_x=5, shrink_y=5):
    rectangle_coordinates = find_color_in_image_rectangle(image_full_location, color)
    if rectangle_coordinates:
        x, y, w, h = rectangle_coordinates
        return click_within_rectangle(x, y, w, h, cropx, cropy, shrink_x, shrink_y)
    return None


def find_color_and_click_polygon(image_full_location, color, cropx, cropy, coordinates):
    polygon = find_closest_color_in_image_precise(image_full_location, color, coordinates)
    if polygon:
        return click_within_polygon(polygon, cropx, cropy)


def take_mining_screenshot_and_find_color_and_click_rectangle(color):
    screen_shot_save_images(image_name="miner_img.png")
    click_coordinates = find_color_and_click_rectangle("images/miner_img.png", color, 0, 30, shrink_x=5, shrink_y=5)
    return click_coordinates


def take_screenshot_and_find_color_and_click_rectangle(color):
    screen_shot_save_images()
    click_coordinates = find_color_and_click_rectangle("images/screenshot.png", color, 0, 30)
    return click_coordinates


def take_combat_screenshot_and_find_color_and_click_closest_polygon(color, coordinates):
    screen_shot_save_images(image_name="combat_img.png")
    # TODO don't attack npcs that are already being attacked
    click_coordinates = find_color_and_click_polygon("images/combat_img.png", color, 0, 30, coordinates)
    return click_coordinates


def inventory_screenshot():
    open_inventory()
    return screen_shot_save_images(620, 480, 820, 750, 'inventshot.png')


def open_inventory():
    inventory_open = is_inventory_open()
    if not inventory_open:
        config.actions = 'opening inventory'
        pyautogui.press('esc')


def is_inventory_open():
    inventory_count = image_count('inventory_enabled.png', threshold=0.95)
    if inventory_count == 1:
        return True
    else:
        return False


def find_image_and_click_rectangles(image_name, shrink_x=5, shrink_y=5, threshold=0.7, clicker='left',
                                    playarea=True,
                                    fast=False):
    if playarea:
        screen_shot_save_images(0, 0, 600, 750)
    else:
        screen_shot_save_images(620, 480, 820, 750)
    loc, template_w, template_v, img_rgb = find_image_in_screenshot(image_name, threshold=threshold)
    click_within_rectangles(loc, template_w, template_v, shrink_x, shrink_y, playarea, clicker, fast)


def loot_all_highlighted_items(live_data_service, current_coordinates):
    # TODO check inventory for space
    if not live_data_service.get_is_inv_full():
        while True:
            screen_shot_save_images(image_name="ground_item.png")
            rectangle_coordinates = find_closest_color_in_image_rectangle("images/ground_item.png", Colors.pickup,
                                                                          current_coordinates, 75)
            if rectangle_coordinates:
                x, y, w, h = rectangle_coordinates
                centroid = (int(x + w / 2), int(y + h / 2))
                if config.image_debugging:
                    debug_image = cv2.imread("images/ground_item.png")
                    cv2.circle(debug_image, centroid, radius=0, color=(0, 255, 255), thickness=4)
                    cv2.imwrite("images/ground_item.png", debug_image)
                move_cursor_and_click((centroid[0], centroid[1] + 30), clicker="right")

                screen_shot_save_images(image_name="find_options_menu.png")
                options_menu_coordinates = find_color_in_image_rectangle("images/find_options_menu.png",
                                                                         Colors.options_menu)
                if options_menu_coordinates:
                    menu_x, menu_y, menu_w, menu_h = options_menu_coordinates

                    screen_shot_save_images(image_name="options_menu.png", min_x=menu_x, min_y=menu_y + 30,
                                            max_x=menu_x + menu_w, max_y=menu_y + menu_h + 30)
                    color_found = find_color_and_click_rectangle("images/options_menu.png", Colors.pickup, menu_x,
                                                                 menu_y + 30)
                    if not color_found:
                        print("Could not find color in options menu")
                        break

                    # TODO I don't think this is the right timing (either of them)
                    time.sleep(0.75)
                    live_data_service.wait_until_idle()
                    # wait for loot highlight to disappear
                    time.sleep(1)

                else:
                    print("Could not find options menu")
            else:
                break


def find_and_click_on_color_in_inventory(color):
    # TODO this doesn't work consistently
    open_inventory()
    coordinates = take_screenshot_and_find_color_and_click_rectangle(color)
    time.sleep(2)
    if not coordinates:
        raise Exception('no food in inventory')


def drop_item():
    pyautogui.keyUp('shift')
    c = random.uniform(0.1, 0.2)
    d = random.uniform(0.1, 0.23)

    time.sleep(c)
    pyautogui.keyDown('shift')
    time.sleep(d)


def release_drop_item():
    e = random.uniform(0.1, 0.3)
    f = random.uniform(0.1, 0.2)

    time.sleep(e)
    pyautogui.keyUp('shift')
    pyautogui.press('shift')
    time.sleep(f)


# TODO Implement this
def startup():
    print('starting up')
