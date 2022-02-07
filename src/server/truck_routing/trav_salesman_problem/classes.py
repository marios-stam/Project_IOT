import json


class Vehicle:
    def __init__(self, vehicle_id, location_id, lon, lat):
        self.vehicle_id = vehicle_id
        self.start_address = {
            "location_id": location_id, "lon": lon, "lat": lat}

    def __repr__(self):
        return json.dumps(self.__dict__)


class Service:
    def __init__(self, service_id, service_name, loc_id, lon, lat):
        self.id = service_id
        self.name = service_name
        self.address = {"location_id": loc_id, "lon": lon, "lat": lat}

    def __repr__(self):
        return json.dumps(self.__dict__)


class Problem:
    def __init__(self) -> None:
        self.vehicles = []
        self.services = []

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)

    def add_service(self, service: Service):
        self.services.append(service)

    def get_json(self):
        self.json_str = str(self.__dict__).replace("'", '"')

        return self.json_str

    def __repr__(self):
        return json.dumps(self.__dict__)
