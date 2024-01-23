import random
from enum import StrEnum

import pyautogui

from common.break_functions import set_new_break_time
from common.config import config_init
from common.live_data import LiveDataService
from common.path_finder import get_path
from common.walker import Walker


class LocationNames(StrEnum):
    GE = 'Grand Exchange',
    AL_KHARID = 'Al Kharid',


locations = {
    LocationNames.GE: (3164, 3484, 0),
    LocationNames.AL_KHARID: (3293, 3183, 0),
}

if __name__ == "__main__":
    # resizeImage()
    config_init()
    x = random.randrange(100, 250)
    y = random.randrange(400, 500)
    pyautogui.click(x, y, button='right')
    set_new_break_time(300, 2000)
    live_data_service = LiveDataService()
    walker = Walker(live_data_service)
    current_location = live_data_service.get_current_location()
    path = get_path(current_location, locations[LocationNames.AL_KHARID])
    walker.better_walk(path)
