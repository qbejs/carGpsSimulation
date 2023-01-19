import pytest

from src.car import Car


@pytest.fixture
def car():
    return Car("Kielce, Zakladowa 2, Poland", "Kielce, Zakladowa 1, Poland")


def test_init(car):
    assert car.route.start_location == "Kielce, Zakladowa 2, Poland"
    assert car.route.end_location == "Kielce, Zakladowa 1, Poland"
    assert car.gps.current_location == None
    assert car.fuel_level == 80
    assert car.fuel_capacity == 80
    assert car.reserve_fuel == 10
    assert car.vehicle_mass == 3.5
    assert car.fuel_efficiency == 8
    assert car.fuel_stops == []


def test_drive(car):
    car.drive()
    assert car.obd.speed != None
    assert car.fuel_level != 80
    assert car.obd.throttle_position != None
    assert car.obd.tire_pressure != None


def test_calculate_speed(car):
    distance = 100
    speed = car.calculate_speed(distance)
    assert speed != None


def test_calculate_fuel_consumption(car):
    distance = 100
    fuel_consumption = car.calculate_fuel_consumption(distance)
    assert fuel_consumption != None
