import json
import random

from common.break_functions import standard_break
from common.client_interaction import move_cursor_and_click, click_options_menu_option
from common.live_data import LiveDataService, LiveDataEndpoints
from common.machine_vision import image_count
from common.resources import BANK_BOOTH_OBJECTS


def get_bank_booth(live_data_service: LiveDataService = LiveDataService()):
    objects = live_data_service.get_live_data(LiveDataEndpoints.OBJECTS)
    bank_booth_ids = BANK_BOOTH_OBJECTS.keys()

    bank_booths = [json.loads(objects[obj])[0] for obj in objects if
                   str(json.loads(objects[obj])[0]['id']) in bank_booth_ids]
    if len(bank_booths) == 0:
        raise Exception('Didnt find bank booth')
    bank_booth = bank_booths[-1]

    return (int(bank_booth['canvas']['x']), int(bank_booth['canvas']['y'])), str(bank_booth['id'])


def open_nearest_bank(live_data_service: LiveDataService = LiveDataService()):
    bank_booth_coordinates, bank_booth_id = get_bank_booth(live_data_service)
    bank_booth = BANK_BOOTH_OBJECTS[bank_booth_id]
    if bank_booth is None:
        raise Exception('Didnt find bank booth')

    if bank_booth['click'] == 'left':
        move_cursor_and_click(bank_booth_coordinates)
    elif bank_booth['click'] == 'right':
        click_options_menu_option(bank_booth_coordinates, bank_booth['open'])


def bank_ready():
    bank = image_count('bank_deposit.png', 0.75)
    if bank > 0:
        return True
    else:
        return False


# These are based on current size of window should be moved to config.
def click_deposit_all():
    x = random.randrange(480, 500)
    y = random.randrange(623, 637)
    move_cursor_and_click((x, y))


def close_bank():
    x = random.randrange(523, 540)
    y = random.randrange(40, 55)
    move_cursor_and_click((x, y))


def open_bank_deposit_all():
    open_nearest_bank()
    bank_open = False
    while not bank_open:
        bank_open = bank_ready()
    standard_break()
    # change to computer vision to work for deposit boxes
    click_deposit_all()
    standard_break()
    # change to computer vision to work for deposit boxes
    close_bank()
    standard_break()
