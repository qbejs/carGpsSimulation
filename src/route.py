class Route:
    def __init__(self, start_location, end_location, geo_service):
        self.start_location = start_location
        self.end_location = end_location
        self.geo_service = geo_service
        self.route = self.geo_service.get_route(start_location, end_location)
        self.speed_limit = self.geo_service.get_speed_limit(self.route)
