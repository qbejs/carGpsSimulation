import osrm

from src.geo_service import GeoService


class GPSDevice:
    def __init__(self):
        self.service = GeoService()
        self.current_location = None
        self.route = None

    def start_navigation(self, route):
        self.route = route
        self.current_location = route[0]

    def stop_navigation(self):
        self.route = None
        self.current_location = None

    def is_arrived(self):
        return self.current_location == self.route[-1]

    def distance_from_prev_step(self, step):
        prev_step = self.current_location
        response = self.service.client.route(
            coordinates=[[prev_step[0], prev_step[1]], [step[0], step[1]]],
            overview=osrm.overview.full,
        )
        distance = response["routes"][0]["distance"]

        return distance
