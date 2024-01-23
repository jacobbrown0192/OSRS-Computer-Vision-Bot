import time

import win32gui
import yaml

with open("./pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

# Configurable Variables
run_duration_hours = 3
image_debugging = True
image_debugging_location = 'images/find_options_menu.png'

# Global Variables
ore = ''
inventory = {}
inventory_count = 0
time_of_last_break = 0
time_to_next_break = 0
time_of_next_break = 0
click_coordinates = (0, 0)
actions = 'None'
status = 'Nothing'
start_time = time.time()
end_time = start_time + (60 * 60 * run_duration_hours)
time_left = 0
window_x = 0
window_y = 0
window_w = 0
window_h = 0
client_top_border = 30
client_side_border = 50
window = (0, 0, 0, 0)

dax_api_key = "sub_DPjXXzL5DeSiPf"
dax_api_secret = "PUBLIC-KEY"

path_cache_file = "path_cache.json"
timer1 = 0
timer2 = 0

# used in the mining_by_checking_on_screen_text function
first_break_for_plugin = True


def get_window(windowname: str) -> list:
    hwnd = win32gui.FindWindow(None, windowname)
    win32gui.SetForegroundWindow(hwnd)
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1] + client_top_border
    w = rect[2] - x - client_side_border
    h = rect[3] - y - client_top_border
    return [x, y, w, h]


# This prevents constantly checking the window for position, we don't expect it to change
def config_init():
    global window_x, window_y, window_w, window_h, window
    window = get_window(data[0]['Config']['client_title'])
    (x, y, w, h) = window
    window_x = x
    window_y = y
    window_w = w
    window_h = h


class ConsoleColors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
