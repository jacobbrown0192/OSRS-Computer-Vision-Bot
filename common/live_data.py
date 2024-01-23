import json
from enum import StrEnum
from time import sleep, time

import requests


class LiveDataEndpoints(StrEnum):
    EVENTS = 'events',
    STATS = "stats",
    INVENTORY = "inv",
    EQUIPMENT = "equip",
    NPC = "npc",
    OBJECTS = "objects",
    DOORS = "doors",
    POST = "post"


class EventCategory(StrEnum):
    ANIMATION = "animation",
    POSE = "animation pose",
    RUN_ENERGY = "run energy",
    TICK = "game tick",
    HEALTH = "health",
    INTERACTION = "interacting code",
    NPC_NAME = "npc name",
    NPC_HEALTH = "npc health ",
    MAX_DISTANCE = "MAX_DISTANCE",
    WORLD_POINT = "worldPoint",
    CAMERA = "camera",
    MOUSE = "mouse"


class LiveDataService:
    data = None

    def __init__(self, host: str = "http://localhost", port: int = 8080, file_buffer: str = None,
                 polling_interval: float = 0.05, debug: bool = False):
        self.port = port
        self.host = host
        self.url_root = f"{self.host}:{self.port}"
        self.file_buffer = file_buffer
        self.polling_interval = polling_interval
        self.debug = debug

    def get_live_data(self, endpoint: LiveDataEndpoints):
        url = f"{self.url_root}/{endpoint}"
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            return []
        return response.json()

    def start_streaming_data(self, endpoint: LiveDataEndpoints):
        while True:
            self.data = self.get_live_data(endpoint)
            if self.debug:
                print(self.data)
            if self.file_buffer:
                self.write_to_file(self.data)
            sleep(self.polling_interval)

    def write_to_file(self, data):
        with open(self.file_buffer, "w+") as outfile:
            json.dump(data, outfile)
        outfile.close()

    def get_event_data(self, event_category: EventCategory):
        data = self.get_live_data(LiveDataEndpoints.EVENTS)
        return data[event_category]

    def get_current_location(self):
        position_data = self.get_event_data(EventCategory.WORLD_POINT)
        return (position_data["x"], position_data["y"], position_data["plane"])

    def wait_until_idle(self):
        while self.get_event_data(EventCategory.POSE) not in [808, 813]:
            sleep(0.05)
            # print('Waiting for idle...')

    def get_is_inv_full(self) -> bool:
        inventory_data = self.get_live_data(LiveDataEndpoints.INVENTORY)
        return len([item["id"] for item in inventory_data if item["id"] != -1]) == 28

    def get_current_health(self) -> int:
        return int(self.get_event_data(EventCategory.HEALTH)["current health"])
