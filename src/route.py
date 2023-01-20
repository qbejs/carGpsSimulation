class Route:
    def __init__(self, start_location, end_location, geo_service):
        self.geo_service = geo_service
        route_data = self.geo_service.get_route(start_location, end_location)
        self.start_location = start_location
        self.end_location = end_location
        self.route = route_data[1]
        self.speed_limit = self.geo_service.get_speed_limit(self.route)
        self.distance = route_data[0]
