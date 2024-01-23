import random
import time
from enum import StrEnum

import pyautogui
from common import config


def random_sleep(minsec, maxsec):
    random_duration = random.uniform(minsec, maxsec)
    time.sleep(random_duration)


def standard_break():
    random_sleep(0.1, 0.7)


def human_break():
    random_triangular_sleep(0.05, 6, 0.5)


def random_triangular_sleep(minsec, maxsec, mode):
    random_duration = random.triangular(minsec, maxsec, mode)
    time.sleep(random_duration)


def random_break_action(time_of_last_break, time_to_break):
    current_time = time.time()
    if current_time - time_of_last_break > time_to_break:
        break_function = random.choice(BREAK_FUNCTION_LIST)
        break_function()
        return True
    else:
        return False


def random_break_action_check(time_of_last_break, time_to_next_break):
    took_break = random_break_action(time_of_last_break, time_to_next_break)
    if took_break:
        set_new_break_time()


def set_new_break_time(minsec=600, maxsec=2000):
    config.time_of_last_break = time.time()
    config.time_to_next_break = random.randrange(minsec, maxsec)
    config.time_of_next_break = config.time_of_last_break + config.time_to_next_break


def random_pause():
    b = random.uniform(20, 250)
    print('pausing for ' + str(b) + ' seconds')
    time.sleep(b)


def open_and_close_tab(key, action):
    config.actions = action
    pyautogui.press(key)
    random_sleep(0.1, 15)
    pyautogui.press(key)
    random_sleep(0.1, 2)
    pyautogui.press('esc')


def random_equipment():
    open_and_close_tab('f4', 'equipment tab')


def random_combat():
    open_and_close_tab('f1', 'combat tab')


def random_skills():
    open_and_close_tab('f2', 'skills tab')


def random_quests():
    open_and_close_tab('f3', 'quests tab')


class BreakFunctionNames(StrEnum):
    RANDOM_INVENTORY = 'random_inventory',
    RANDOM_COMBAT = 'random_combat',
    RANDOM_SKILLS = 'random_skills',
    RANDOM_QUESTS = 'random_quests',
    RANDOM_PAUSE = 'random_pause'


BREAK_FUNCTIONS = {
    BreakFunctionNames.RANDOM_INVENTORY: random_equipment,
    BreakFunctionNames.RANDOM_COMBAT: random_combat,
    BreakFunctionNames.RANDOM_SKILLS: random_skills,
    BreakFunctionNames.RANDOM_QUESTS: random_quests,
    BreakFunctionNames.RANDOM_PAUSE: random_pause,
}

BREAK_FUNCTION_LIST = list(BREAK_FUNCTIONS.values())
