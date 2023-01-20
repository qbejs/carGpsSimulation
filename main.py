import concurrent.futures
from rich.console import Console

from src.car import Car
import pandas


def drive_lambda(car):
    car.drive()


if __name__ == '__main__':
    console = Console()
    console.print("Reading csv file...")
    result = pandas.read_csv('list.csv', delimiter=';')
    cars = (result.apply(lambda x: Car(x['start_location'], x['end_location']),
                         axis=1).tolist())
    console.print("Cars prepared. Let's get started...")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(drive_lambda, car) for car in cars]
        for future in concurrent.futures.as_completed(futures):
            future.result()
