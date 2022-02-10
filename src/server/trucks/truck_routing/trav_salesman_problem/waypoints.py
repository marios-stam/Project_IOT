import json
import os
from unittest import result


def extract_waypoints_from_result():
    # load json file
    result_file_name = os.path.join(os.getcwd(), "server/trucks/truck_routing/trav_salesman_problem/result.json")
    with open(result_file_name) as f:
        data = json.load(f)

    # extract waypoints

    routes = data["solution"]["routes"]
    trucks_routes = []
    for route in routes:
        waypoints = route["activities"]

        coords_list = []
        for wp in waypoints:
            loc_id = wp["address"]["location_id"]
            lon = wp["address"]["lon"]
            lat = wp["address"]["lat"]

            coords_list.append({"loc_id": loc_id, "lon": lon, "lat": lat})

        # print(coords_list)
        dictionary = {
            "truck_id": route["vehicle_id"], "waypoints": coords_list[:-1]}

        trucks_routes.append(dictionary)

    # for route in trucks_routes:
    #     print("truck_id:", route["truck_id"])
    #     for wp in route["waypoints"]:
    #         print(wp)

    #     print("============================")

    return trucks_routes


if __name__ == '__main__':
    extract_waypoints_from_result()
