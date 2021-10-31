from typing import List

from garage.parking_level import ParkingLevel
from garage.permit import Permit
from garage.vehicle import Vehicle
from garage.vehicle_type import VehicleType


class Garage:
    levels: List[ParkingLevel]

    def __init__(self, levels: List[ParkingLevel] = None):
        self.levels = levels or []

    def add_vehicles(self, vehicles: List[Vehicle] = None) -> List[Vehicle]:
        rejected = []
        sorted_vehicles = self.sort_vehicles(vehicles)
        for vehicle in sorted_vehicles:
            if not self.add_vehicle(vehicle):
                rejected.append(vehicle)

        # Have to unsort reject list for test 3_1
        out = []
        for vehicle in vehicles:
            if vehicle in rejected:
                out.append(vehicle)
        return out

    def add_vehicle(self, vehicle):
        # First handle Disability
        if Permit.DISABILITY in vehicle.permit:
            if self.add_permit(vehicle, Permit.DISABILITY):
                return True

        # Next handle premium parking
        if Permit.PREMIUM in vehicle.permit:
            if self.add_permit(vehicle, Permit.PREMIUM):
                return True

        # If the vehicle is compact, prioritize compact spots
        if vehicle.vehicle_type == VehicleType.Compact:
            if self.add_compact(vehicle):
                return True
        
        # Add any other vehicles
        for level in self.levels:
                for space in level.spaces:
                    if space.vehicle == None:
                        if not space.compact:
                            if space.required_permit == Permit.NONE:
                                space.vehicle = vehicle
                                return True
        return False

    def sort_vehicles(self, vehicles):
        # Sort the vehicles by priority, dual -> premium -> other
        dual = []
        premium = []
        other = []
        for vehicle in vehicles:
            if Permit.DISABILITY in vehicle.permit and Permit.PREMIUM in vehicle.permit:
                dual.append(vehicle)
            elif Permit.PREMIUM in vehicle.permit:
                premium.append(vehicle)
            else:
                other.append(vehicle)
        
        out = dual + premium + other
        return out


    def add_compact(self, vehicle):
        for level in self.levels:
                for space in level.spaces:
                    if space.vehicle == None:
                        if space.compact:
                            if vehicle.vehicle_type == VehicleType.Compact:
                                space.vehicle = vehicle
                                return True
        return False
    
    def add_permit(self, vehicle, permit):
        for level in self.levels:
                for space in level.spaces:
                    if space.vehicle == None:
                        if space.required_permit == permit:
                            space.vehicle = vehicle
                            return True
        return False        