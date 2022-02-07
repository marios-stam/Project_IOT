import json


def extract_waypoints_from_result():
    # load json file
    with open('result.json') as f:
        data = json.load(f)

    # extract waypoints

    waypoints = data["solution"]["routes"][0]["activities"]
    coords_list = []
    for wp in waypoints:
        loc_id = wp["address"]["location_id"]
        lon = wp["address"]["lon"]
        lat = wp["address"]["lat"]

        print(loc_id, lon, lat)
        coords_list.append({"loc_id": loc_id, "lon": lon, "lat": lat})

    print(coords_list)


if __name__ == '__main__':
    extract_waypoints_from_result()
