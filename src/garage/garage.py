from typing import List

from garage.parking_level import ParkingLevel
from garage.vehicle import Vehicle


class Garage:
    levels: List[ParkingLevel]

    def __init__(self, levels: List[ParkingLevel] = None):
        self.levels = levels or []

    def add_vehicles(self, vehicles: List[Vehicle] = None) -> List[Vehicle]:
        rejected = []
        for vehicle in vehicles:
            if self.add_vehicle(vehicle) is False:
                rejected.append(vehicle)
        return rejected

    def add_vehicle(self, vehicle):
        for level in self.levels:
                for space in level.spaces:
                    if space.vehicle == None:
                        space.vehicle = vehicle
                        return True
        return False
