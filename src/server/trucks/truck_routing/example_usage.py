import os
from .trav_salesman_problem import get_waypoints_for_each_truck
from .mapbox import calculate_route_from_waypoints
import json


def fleet_route_optimising(trucks, bins_to_collect):
    """
    trucks : list of (truck_id,longitude,latitude)
    bins_to_collect : list of (bin_id,longitude,latitude)
    """
    routes = get_waypoints_for_each_truck(trucks, bins_to_collect)

    total_result = []
    for route in routes:
        print("truck_id:", route["truck_id"])

        start = (route["waypoints"][0]["lon"], route["waypoints"][0]["lat"])

        wps = []
        for wp in route["waypoints"][1:]:
            wps.append((wp["lon"], wp["lat"]))

        # limit array to 25 elements(23+2)
        wps = wps[:23]
        print("wps length:", len(wps))

        route_with_wps = calculate_route_from_waypoints(start, wps)
        print("mlkia route_with_wps:", route_with_wps)

        route_coords = route_with_wps["routes"][0]["geometry"]["coordinates"]

        steps = route_with_wps["routes"][0]["legs"]

        dictionary = {
            "truck_id": route["truck_id"],
            "route_coords": route_coords,
            "steps": steps, }

        total_result.append(dictionary)

    total_result_file_name = os.path.join(
        os.getcwd(), "server/trucks/truck_routing/total_result.json")
    with open(total_result_file_name, 'w') as outfile:
        outfile.write(json.dumps(total_result))

    return total_result


if __name__ == "__main__":
    trucks = [
        ("truck_id1", 9.997, 53.551),
        ("truck_id2", 11.57, 48.144)
    ]

    bins_to_collect = [
        (9.999, 53.552), (9.998, 53.553),
        (11.57, 48.145), (11.56, 48.146)
    ]

    fleet_route_optimising(trucks, bins_to_collect)
