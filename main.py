from rich.console import Console

from src.car import Car

if __name__ == '__main__':
    console = Console()
    console.print("Enter start address (Country, City, Street)")
    start_point = input()
    console.print("Enter end address (Country, City, Street)")
    end_point = input()

    car = Car(start_point, end_point)
    car.drive()
