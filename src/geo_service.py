import json
from random import Random

import osrm
import requests


class GeoService:
    client: osrm
    randomizer: Random

    def __init__(self):
        self.client = osrm.Client(host="https://router.project-osrm.org")
        self.randomizer = Random()

    def geocode(self, location):
        url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
        response = requests.get(url, timeout=90)
        data = json.loads(response.text)
        return [float(data[0]["lon"]), float(data[0]["lat"])]

    def get_route(self, start_location, end_location):
        start_coords = self.geocode(start_location)
        end_coords = self.geocode(end_location)
        response = self.client.route(
            coordinates=[start_coords, end_coords], overview=osrm.overview.full
        )

        if (
                "routes" in response
                and "geometry" in response["routes"][0]
                and "coordinates" in response["routes"][0]["geometry"]
        ):
            return [
                response["routes"][0]["legs"][0]["distance"],
                response["routes"][0]["geometry"]["coordinates"]
            ]

        raise Exception(
            f"Cannot retrieve route from project-osrm.org. Details: {response}] "
        )

    def get_speed_limit(self, route) -> int:
        # To refactor. Goal is to find actual speed limit based on route geometry coordinates
        return 60
