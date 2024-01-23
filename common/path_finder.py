import json
import random

import requests

from common import config

DAX_API_URL = "https://api.dax.cloud"
DAX_PATH_URL = DAX_API_URL + "/walker/generatePath"
DAX_BANK_PATH_URL = DAX_API_URL + "/walker/generateBankPath"


def generate_dax_header():
    return {
        "key": config.dax_api_key,
        "secret": config.dax_api_secret
    }


# TODO remove other forms of transport from the request
def get_path_from_dax(start, end):
    headers = generate_dax_header()
    start_end_coordinates = {
        "start": {
            "x": start[0],
            "y": start[1],
            "z": start[2]
        },
        "end": {
            "x": end[0],
            "y": end[1],
            "z": end[2]
        }
    }
    response = requests.post(DAX_PATH_URL, json=start_end_coordinates, headers=headers)
    # todo: handle error correctly, this doesn't work
    if response.status_code != 200:
        raise Exception(f"Error while getting path from DAX: {response.text}")
    result = response.text
    return result


def get_bank_path_from_dax(start, end):
    headers = generate_dax_header()
    start_coordinates_and_bank = {
        "start": {
            "x": start[0],
            "y": start[1],
            "z": start[2]
        },
        "end": {
            "x": end[0],
            "y": end[1],
            "z": end[2]
        }
    }
    response = requests.post(DAX_BANK_PATH_URL, json=start_coordinates_and_bank, headers=headers)
    result = response.text
    return result


def open_cache_file():
    try:
        with open(config.path_cache_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def store_path_in_cache_file(key, value):
    # key = f"{start[0]}-{start[1]}-{start[2]}-{end[0]}-{end[1]}-{end[2]}"
    cache = open_cache_file()
    cache[key] = value
    with open(config.path_cache_file, "w") as f:
        json.dump(cache, f)


def get_path_from_cache_file(key):
    # key = f"{start[0]}-{start[1]}-{start[2]}-{end[0]}-{end[1]}-{end[2]}"
    cache = open_cache_file()
    if key in cache:
        return cache[key]
    return None


def get_path(start, end):
    key = f"{start[0]}-{start[1]}-{start[2]}-{end[0]}-{end[1]}-{end[2]}"
    path = get_path_from_cache_file(key)
    if path is None:
        path = get_path_from_dax(start, end)
        store_path_in_cache_file(key, path)
    dict_path = json.loads(path)
    return dict_path['path']


def get_optimized_path(start, end):
    path = get_path(start, end)
    return optimize_path(path)


def optimize_path(path, randomize=False):
    max_path_distance = 18  # max possible value is 19
    optimized_path = [path[0]]
    last_selected_coordinate = path[0]
    for path_index, coordinate in enumerate(path):
        distance = abs(coordinate['x'] - last_selected_coordinate['x']) + abs(
            coordinate['y'] - last_selected_coordinate['y'])

        if coordinate['z'] != last_selected_coordinate['z']:
            # If the coordinate is on a different floor, want to add the last possible coordinate on the current floor
            if last_selected_coordinate != path[path_index - 1]:
                optimized_path.append(path[path_index - 1])
            optimized_path.append(coordinate)
            last_selected_coordinate = coordinate
        if distance == max_path_distance:
            optimized_path.append(coordinate)
            last_selected_coordinate = coordinate
        if distance > max_path_distance:
            optimized_path.append(path[path_index - 1])
            last_selected_coordinate = path[path_index - 1]

            distance = abs(coordinate['x'] - last_selected_coordinate['x']) + abs(
                coordinate['y'] - last_selected_coordinate['y'])

            if coordinate['z'] != last_selected_coordinate['z']:
                # If the coordinate is on a different floor, want to add the last possible coordinate on the current floor
                if last_selected_coordinate != path[path_index - 1]:
                    optimized_path.append(path[path_index - 1])
                optimized_path.append(coordinate)
                last_selected_coordinate = coordinate
            if distance == max_path_distance:
                optimized_path.append(coordinate)
                last_selected_coordinate = coordinate
            if distance > max_path_distance:
                raise Exception("distance between two path points is greater than max_path_distance")
    if optimized_path[-1] != path[-1]:
        optimized_path.append(path[-1])
    return optimized_path


# TODO we don't need to be right next to the stairs to use them,
#  so we can optimize the path to be more efficient and have a z change max distance as well
def get_next_optimized_path_point(path, current_position, randomize=False):
    max_path_distance = 18  # max possible value is 19
    max_z_path_distance = 7  # unsure max value
    path_distance = max_z_path_distance
    if randomize:
        path_distance = random.randrange(15, max_path_distance)
    last_selected_coordinate = {'x': current_position['x'], 'y': current_position['y'], 'z': current_position['plane']}
    for path_index, coordinate in enumerate(path):
        distance = abs(coordinate['x'] - last_selected_coordinate['x']) + abs(
            coordinate['y'] - last_selected_coordinate['y'])

        if path_index == len(path) - 1:
            return PathPoint(*coordinate.values(), True), path[path_index:]

        if coordinate['z'] != last_selected_coordinate['z']:
            if distance > max_z_path_distance:
                if last_selected_coordinate != path[path_index - 1]:
                    return PathPoint(*path[path_index - 1].values(), True), path[path_index - 1:]
            return PathPoint(*coordinate.values()), path[path_index:]

        if distance == path_distance:
            required = False
            if coordinate['z'] != path[path_index + 1]['z']:
                required = True
            return PathPoint(*coordinate.values(), required), path[path_index:]

        if distance > path_distance:
            required = False
            if coordinate['z'] != path[path_index + 1]['z']:
                required = True
            # This shouldn't happen now
            if path_index == 0:
                print('path_index == 0')
                return PathPoint(*coordinate.values(), required), path[path_index:]
            return PathPoint(*path[path_index - 1].values(), required), path[path_index - 1:]


class PathPoint:
    def __init__(self, x, y, z, required_stop=False):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.required_stop = required_stop

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))
