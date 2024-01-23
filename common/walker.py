import copy
import json
import math
import random
import time

from common import config
from common.client_interaction import random_duration_interaction, Interactions, move_cursor_and_click, \
    click_options_menu_option

from common.live_data import LiveDataService, EventCategory, LiveDataEndpoints
from common.path_finder import get_next_optimized_path_point
from common.resources import STAIRS_OBJECTS


def stairs_canvas_special_cases(stairs_x, stairs_y, object_id):
    if object_id == '16673':
        return stairs_x, stairs_y + 10
    else:
        return stairs_x, stairs_y


class Walker:
    client_top_border = 30
    client_side_border = 50
    tiles_pixels = 4
    offset_minimap_x = 377.0
    offset_minimap_y = 195.0
    offset_minimap_x_resize = 72
    offset_minimap_y_resize = 81
    offset_run_button_x = 150
    offset_run_button_y = 130
    offset_logout_x = 10
    offset_logout_y = 10
    degreesPerYaw: float = 360 / 2048
    is_run = False

    def __init__(self, live_data_service: LiveDataService = LiveDataService()):
        self.live_data_service = live_data_service

    def get_run_button(self, window_features: list) -> list:
        x, y, w, h = window_features
        run_x = x + (w - self.offset_run_button_x)
        run_y = y + self.offset_run_button_y
        return [run_x, run_y]

    def get_logout_cross(self, window_features: list) -> list:
        x, y, w, h = window_features
        run_x = x + (w - self.offset_logout_x)
        run_y = y + self.offset_logout_y
        return [run_x, run_y]

    def find_center_minimap_resizable(self, window_features: list) -> list:
        '''Returns the center of the window, excluding the borders.'''
        x, y, w, h = window_features
        map_center_x = x + (w - self.offset_minimap_x_resize)
        map_center_y = y + self.offset_minimap_y_resize
        return [map_center_x, map_center_y]

    # TODO, compute tiles takes 0.01 seconds, so tiles are off,
    #  could put an offset if not fully stopping and if running or not
    def compute_tiles(self, new_x: int, n_y: int) -> list:
        '''Returns the range to click from the minimap center in amount of tiles.'''
        # Get live camera data.
        camera_data = self.live_data_service.get_event_data(EventCategory.CAMERA)
        current_position = self.live_data_service.get_event_data(EventCategory.WORLD_POINT)
        live_x, live_y = current_position['x'], current_position['y']
        if camera_data is not None:
            yaw = camera_data['yaw']
            degrees = 360 - self.degreesPerYaw * yaw
            theta = math.radians(degrees)
            x_reg = (new_x - live_x) * self.tiles_pixels
            y_reg = (live_y - n_y) * self.tiles_pixels
            tiles_x = x_reg * math.cos(theta) + y_reg * math.sin(theta)
            tiles_y = -x_reg * math.sin(theta) + y_reg * math.cos(theta)
            return [round(tiles_x, 1), round(tiles_y, 1)]
        return [live_x, live_y]

    def change_position(self, center_mini: list, live_pos: list, new_pos: list, required_stop: bool = False):
        '''Clicks the minimap to change position'''
        # Check for max number of tiles to traverse
        tiles = self.compute_tiles(new_pos[0], new_pos[1])
        new_minimap_coordinates = (center_mini[0] + tiles[0], center_mini[1] + tiles[1])
        random_duration_interaction(new_minimap_coordinates, Interactions.click, instant=True)

        # wait until walking starts
        if required_stop:
            time.sleep(1)
            self.live_data_service.wait_until_idle()
        else:
            self.wait_until_close(new_pos[0], new_pos[1])
        position_data = self.live_data_service.get_event_data(EventCategory.WORLD_POINT)
        live_x, live_y = position_data['x'], position_data['y']
        if abs(new_pos[0] - live_x) != 0 or abs(new_pos[1] - live_y) != 0:
            print('something went wrong when walking to the right place')
            if required_stop:
                self.change_position(center_mini, live_pos, new_pos, required_stop)

    def wait_until_close(self, new_x: int, new_y: int):
        t_end = time.time() + random.randrange(10, 15)
        # we wait here so that the bot has time to start walking and doesn't short circuit
        time.sleep(1)
        position_data = self.live_data_service.get_event_data(EventCategory.WORLD_POINT)
        live_x, live_y = position_data['x'], position_data['y']
        while abs(new_x - live_x) > 2 or abs(new_y - live_y) > 2:
            if time.time() > t_end:
                print(time.time(), "| ", t_end)
                break
            if self.live_data_service.get_event_data(EventCategory.POSE) in [808, 813]:
                break
            time.sleep(0.1)
            position_data = self.live_data_service.get_event_data(EventCategory.WORLD_POINT)
            live_x, live_y = position_data['x'], position_data['y']

    def toggle_run(self) -> None:
        """Turns on run energy."""
        run_on = self.get_run_button(config.window)
        x = run_on[0] + random.randrange(-3, 3)
        y = run_on[1] + random.randrange(-3, 3)
        random_duration_interaction((x, y), Interactions.moveTo)
        random_duration_interaction((x, y), Interactions.click)

    # combine this with computer vision
    def handle_running(self) -> None:
        """Turns on run if run energy is higher than 60."""
        run_energy = self.live_data_service.get_event_data(EventCategory.RUN_ENERGY)
        while run_energy is None:
            run_energy = self.live_data_service.get_event_data(EventCategory.RUN_ENERGY)
        if run_energy < 500 or run_energy == 10000:
            self.is_run = False
        if run_energy > 6000 and self.is_run is False:
            self.toggle_run()
            self.is_run = True

    def better_walk(self, path):
        '''Walks a path by clicking on the minimap'''
        center_minimap = self.find_center_minimap_resizable(config.window)
        random_duration_interaction(center_minimap, Interactions.click, fast=True)
        position_data = self.live_data_service.get_event_data(EventCategory.WORLD_POINT)
        while position_data is None:
            position_data = self.live_data_service.get_event_data(EventCategory.WORLD_POINT)
        current_position = [position_data['x'], position_data['y']]
        current_coordinate = position_data
        finish_walk = False

        walk_path = copy.deepcopy(path)

        # Walk while path has coordinates.
        while not finish_walk:
            path_coordinate, walk_path = get_next_optimized_path_point(walk_path, current_coordinate, True)

            if path_coordinate.z != current_coordinate['plane']:
                # Change floors.
                self.live_data_service.wait_until_idle()
                # come to complete stop
                time.sleep(1)
                self.change_floor(current_coordinate, path_coordinate)
                time.sleep(2)
            else:
                self.handle_running()
                path_x = path_coordinate.x
                path_y = path_coordinate.y
                x_y_coordinate = (path_x, path_y)
                self.change_position(center_minimap, current_position, x_y_coordinate, path_coordinate.required_stop)
            # Update position data.
            current_coordinate = self.live_data_service.get_event_data(EventCategory.WORLD_POINT)
            current_position = [current_coordinate['x'], current_coordinate['y']]
            print(current_position)
            if not walk_path or len(walk_path) == 1:
                finish_walk = True
        # wait for full stop
        time.sleep(1)

    def change_floor(self, current_coordinate, next_coordinate):
        direction = next_coordinate.z - current_coordinate['plane']
        stairs_coordinates, object_id = self.get_stairs(current_coordinate)
        stairs = STAIRS_OBJECTS[object_id]
        if stairs is None:
            raise Exception('Didnt find stairs')
        if stairs['click'] == 'left':
            move_cursor_and_click(stairs_coordinates, click_delay=0.3)
        elif stairs['click'] == 'right':
            if direction > 0:
                click_options_menu_option(stairs_coordinates, stairs['up'])
            elif direction < 0:
                click_options_menu_option(stairs_coordinates, stairs['down'])

    def get_stairs(self, current_coordinate):
        objects = self.live_data_service.get_live_data(LiveDataEndpoints.OBJECTS)
        stairs_ids = STAIRS_OBJECTS.keys()

        stairs = [json.loads(objects[obj])[0] for obj in objects if
                  str(json.loads(objects[obj])[0]['id']) in stairs_ids]
        if not stairs:
            raise Exception('Didnt find stairs')
        staircase = stairs[-1]

        stairs_x, stairs_y = stairs_canvas_special_cases(int(staircase['canvas']['x']), int(staircase['canvas']['y']),
                                                         str(staircase['id']))

        return (stairs_x, stairs_y), str(staircase['id'])
