import random
import time
from datetime import datetime
from enum import StrEnum

import pyautogui

from common import config
from common.banking import open_bank_deposit_all
from common.break_functions import random_sleep, random_break_action_check, set_new_break_time, \
    human_break
from common.common_functions import start_timer_countdown_loop, break_message, \
    take_mining_screenshot_and_find_color_and_click_rectangle, open_inventory, \
    find_image_and_click_rectangles, get_inventory
from common.config import config_init, ConsoleColors
from common.live_data import LiveDataService, EventCategory
from common.machine_vision import image_to_text, image_count, Colors
from common.path_finder import get_path
from common.resources import BANK_NAMES, bank_locations
from common.walker import Walker
from sly_scripts.functions import drop_item
from sly_scripts.functions import release_drop_item


# could make this generic to with a drop and keep lists.
def drop_ore(ore):
    open_inventory()
    drop_item()
    find_image_and_click_rectangles(ore + '_ore.png', threshold=0.8, playarea=False)
    release_drop_item()


def debug_message(end_time, click_coordinates, status, ore, actions):
    time_left = str(datetime.timedelta(seconds=round(end_time - time.time(), 0)))
    print(ConsoleColors.WARNING +
          f'\rtime left: {time_left} | coords: {click_coordinates} | status: {status} | ore: {ore} | gems: {int(image_count("gem_icon.png") + image_count("gem_icon2.png"))} | clues: {int(image_count("geo_icon.png"))} | {actions}',
          end='')


def print_mining_progress():
    current_time = time.time()
    time_left = config.end_time - current_time
    percent_left = time_left / (config.end_time - config.start_time)
    print(ConsoleColors.OK + f'\r[%-10s] %d%%' % ('=' * round(percent_left * 10), round(percent_left * 100)),
          f'\rtime left: {time_left / 60 :.2f} mins | coords: {config.click_coordinates} | status: {config.status} | ore: {get_inventory("ore_count")} | gems: {get_inventory("gem_count")} | clues: {get_inventory("clue_count")} | {config.actions}',
          end='')


#   deprecated in favor of the new live data service
def count_mining_inventory():
    open_inventory()
    config.inventory['gem_count'] = int(image_count("gem_icon.png") + image_count("gem_icon2.png"))
    config.inventory['ore_count'] = int(image_count(config.ore + '_ore.png'))
    config.inventory['clue_count'] = int(image_count("geo_icon.png"))
    config.inventory_count = get_inventory("gem_count") + get_inventory("ore_count") + get_inventory("clue_count")
    return config.inventory_count


def mining_by_checking_on_screen_text(take_human_break=False, color=Colors.green):
    mining_image_text = image_to_text('thresh')
    if mining_image_text.strip().lower() != 'mining':
        config.status = 'Not Mining'
        if take_human_break:
            config.status = 'Taking Human Break'
            human_break()
        config.click_coordinates = take_mining_screenshot_and_find_color_and_click_rectangle(color)
        # wait for mining to start
        config.status = 'Waiting for Mining to Start'
        time.sleep(2)
    else:
        config.status = 'Mining'
    if config.first_break_for_plugin:
        config.status = 'Taking First Break'
        random_sleep(2, 3)
        config.first_break_for_plugin = False


def basic_color_miner(ore, color, take_human_break=False, run_duration_hours=5, store_bank=None):
    config.ore = ore
    break_message(config.time_to_next_break)
    # This thread acts as an event loop
    start_timer_countdown_loop(print_mining_progress)
    live_data_service = LiveDataService()
    walker = Walker(live_data_service)
    config.actions = 'None'

    end_time = time.time() + (60 * 60 * run_duration_hours)
    while time.time() < end_time:
        random_break_action_check(config.time_of_last_break, config.time_to_next_break)
        inventory_full = live_data_service.get_is_inv_full()
        if not store_bank and inventory_full:
            config.actions = 'dropping ore starting...'
            drop_ore(ore)
            config.actions = 'dropping ore finished'
            random_sleep(0.2, 0.7)
            # debug_message(end_time, click_coordinates, status, ore, actions)
        if store_bank and inventory_full:
            config.actions = 'Bank Inventory'
            current_location = live_data_service.get_current_location()
            path = get_path(current_location, bank_locations[store_bank])
            walker.better_walk(path)
            open_bank_deposit_all()
            config.actions = 'Walk Back to Mining Spot'
            path = get_path(bank_locations[store_bank], current_location)
            walker.better_walk(path)
        if live_data_service.get_event_data(EventCategory.ANIMATION) != -1:
            config.status = 'Mining'
            while live_data_service.get_event_data(EventCategory.ANIMATION) != -1:
                time.sleep(0.1)
            if take_human_break:
                config.status = 'Taking Human Break'
                human_break()
            config.status = 'Not Mining'

        config.click_coordinates = take_mining_screenshot_and_find_color_and_click_rectangle(color)
        # wait for mining to start
        config.status = 'Waiting for Mining to Start'
        time.sleep(1.5)


# -------------------------------

class Ores(StrEnum):
    tin = 'tin',
    copper = 'copper',
    coal = 'coal',
    iron = 'iron',
    gold = 'gold',
    clay = 'clay',


ORE_COLOR_BOUNDARIES = {
    Ores.tin: ([103, 86, 65], [145, 133, 128]),
    Ores.copper: ([35, 70, 120], [65, 110, 170]),
    Ores.coal: ([20, 30, 30], [30, 50, 50]),
    Ores.iron: ([15, 20, 40], [25, 40, 70]),  # iron2 = ([17, 20, 42], [25, 38, 70])
    Ores.gold: None,
    Ores.clay: ([50, 105, 145], [60, 125, 165]),
}

if __name__ == "__main__":
    # resizeImage()
    config_init()
    x = random.randrange(100, 250)
    y = random.randrange(400, 500)
    pyautogui.click(x, y, button='right')
    set_new_break_time(300, 2000)

    basic_color_miner(Ores.tin, Colors.mining_blue, take_human_break=True, run_duration_hours=config.run_duration_hours,
                      store_bank=BANK_NAMES.AL_KHARID_PVP_CHESTS)
