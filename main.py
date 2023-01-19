import time

from rich.console import Console
from rich.progress import track

from src.car import Car

if __name__ == '__main__':
    console = Console()
    console.print("Podaj adres startu")
    start_point = input()
    console.print("Podaj adres docelowy")
    end_point = input()

    car = Car(start_point, end_point)
    car.drive()
