import math
import random
from datetime import datetime, timedelta

import numpy as np
from rich import box
from rich.console import Console
from rich.table import Table
from tqdm import tqdm

from src.geo_service import GeoService
from src.gps_device import GPSDevice
from src.obd_device import OBDDevice
from src.route import Route


class Car:
    def __init__(self, start_location, end_location):
        self.route = Route(start_location, end_location, GeoService())
        self.gps = GPSDevice()
        self.obd = OBDDevice()
        self.fuel_level = 80  # Starting fuel level in liters
        self.fuel_capacity = 80  # Fuel tank capacity in liters
        self.reserve_fuel = 10  # Reserve fuel level in liters
        self.vehicle_mass = 3.5  # Mass of the vehicle in tons
        self.fuel_efficiency = 8  # liters/100km
        self.current_speed = 0
        self.distance_counter = 0
        self.fuel_stops = []
        self.speed_interpolation = np.linspace(0, self.route.speed_limit*28, int(self.route.distance))
        self.status = ['OK', 'MIL_CHECK', 'STOP']

    def drive(self):
        self.gps.start_navigation(self.route.route)
        start_time = datetime.now()
        dys = self.route.distance
        console = Console()
        console.print(f"Started_at={start_time}")
        console.print(f"Distance={self.route.distance}")
        table = Table(title="Route summary", box=box.HEAVY, expand=True)
        table.add_column("Speed (kmh)", justify="center", no_wrap=True)
        table.add_column("Throttle (%)", justify="center", no_wrap=True)
        table.add_column("Fuel (%)", justify="center", no_wrap=True)
        table.add_column("Tire (psi)", justify="center")
        table.add_column("Distance(m)", justify="center", no_wrap=True)
        table.add_column("Position", justify="center")
        table.add_column("OBD Status", justify="center", no_wrap=True)

        for step in tqdm(self.route.route):
            distance = self.gps.distance_from_prev_step(step)
            dys = dys - distance
            self.obd.speed = self.calculate_speed(distance)
            self.fuel_level -= self.calculate_fuel_consumption(distance)
            if self.fuel_level <= 0:
                fuel_stop_start = datetime.now()
                self.fuel_stops.append(
                    {
                        "location": self.gps.current_location,
                        "start_time": fuel_stop_start,
                        "end_time": fuel_stop_start + timedelta(minutes=5),
                    }
                )
                self.fuel_level = self.fuel_capacity

            table.add_row(
                str(round(self.obd.speed)),
                str(random.randint(25, 90)),
                str(round(self.fuel_level)),
                f"OK {self.generate_tire_pressure()}",
                str(round(dys, 2)),
                str(step),
                str(random.choices(self.status, weights=(80, 10, 1), k=1))
            )
            self.gps.current_location = step

        self.gps.stop_navigation()
        console.print(table)
        console.print(self.fuel_stops)

    def calculate_speed(self, distance):
        self.current_speed = self.speed_interpolation[int(self.distance_counter)]
        self.distance_counter += 1
        return self.current_speed

    def calculate_fuel_consumption(self, distance):
        # calculate the fuel consumption based on the distance and vehicle speed
        speed = self.obd.speed
        fuel_consumption = (distance / 100) * (self.fuel_efficiency + (speed * 0.01))
        return fuel_consumption

    def generate_tire_pressure(self) -> list:
        return random.sample(range(37, 42), 4)
