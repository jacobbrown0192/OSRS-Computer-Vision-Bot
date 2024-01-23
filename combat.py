import random
import time

import pyautogui

from common import config
from common.break_functions import set_new_break_time, random_break_action_check, human_break
from common.common_functions import break_message, start_timer_countdown_loop, \
    take_combat_screenshot_and_find_color_and_click_closest_polygon, loot_all_highlighted_items, \
    find_and_click_on_color_in_inventory, startup
from common.config import config_init, ConsoleColors
from common.live_data import LiveDataService, EventCategory
from common.machine_vision import Colors


def print_combat_progress():
    current_time = time.time()
    time_left = config.end_time - current_time
    percent_left = time_left / (config.end_time - config.start_time)
    print(ConsoleColors.OK + f'\r[%-10s] %d%%' % ('=' * round(percent_left * 10), round(percent_left * 100)),
          f'\rtime left: {time_left / 60 :.2f} mins | coords: {config.click_coordinates} | status: {config.status} | {config.actions}',
          end='')


def basic_color_combat(bury_bones=True, pickup_loot=False, take_human_break=False,
                       run_duration_hours=6, attack_npc_by_name=False, attack_npc_by_color=False,
                       wait_for_loot_after_each_kill=False, health_threshold=0):
    break_message(config.time_to_next_break)
    start_timer_countdown_loop(print_combat_progress)
    live_data_service = LiveDataService()

    end_time = time.time() + (60 * 60 * run_duration_hours)
    current_position = live_data_service.get_event_data(EventCategory.WORLD_POINT)
    current_canvas_coordinates = (current_position['canvas_x'], current_position['canvas_y'])

    while time.time() < end_time:
        # timeout after 60 seconds of not being in combat, could be trying to attack an npc that is not attackable
        random_break_action_check(config.time_of_last_break, config.time_to_next_break)
        if live_data_service.get_event_data(EventCategory.NPC_NAME) != 'null':
            config.status = 'in combat with ' + live_data_service.get_event_data(EventCategory.NPC_NAME)
            while live_data_service.get_event_data(EventCategory.NPC_NAME) != 'null':
                time.sleep(0.1)
                if live_data_service.get_current_health() < health_threshold:
                    config.status = 'health is low, eating food'
                    find_and_click_on_color_in_inventory(Colors.blue)
            if pickup_loot:
                config.status = 'Picking up loot'
                if wait_for_loot_after_each_kill:
                    # wait for loot to be highlighted
                    time.sleep(2.5)
                # TODO This fails if two looting spots are next to each other
                loot_all_highlighted_items(live_data_service, current_canvas_coordinates)
            if bury_bones:
                config.status = 'Burying bones'
                # TODO bury bones randomizer, wait for a random amount of bones to be in inventory
            if take_human_break:
                config.status = 'Taking Human Break'
                human_break()

        # attack closest monster
        if attack_npc_by_name:
            time.sleep(0.1)
        if attack_npc_by_color:
            config.status = 'Attacking closest monster'
            config.click_coordinates = take_combat_screenshot_and_find_color_and_click_closest_polygon(
                Colors.attack_blue, current_canvas_coordinates)
            time.sleep(0.8)


if __name__ == "__main__":
    startup()
    config_init()
    x = random.randrange(100, 250)
    y = random.randrange(400, 500)
    set_new_break_time(300, 2000)
    pyautogui.click(x, y, button='right')

    basic_color_combat(take_human_break=True, pickup_loot=True, attack_npc_by_color=True,
                       run_duration_hours=config.run_duration_hours, health_threshold=10)
