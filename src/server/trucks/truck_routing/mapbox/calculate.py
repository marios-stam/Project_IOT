import requests
import json


def load_key():  # load key from .txt file
    with open(r"src\server\trucks\truck_routing\mapbox\api_key.txt", "r") as key_file:
        key = key_file.read()
    return key


# print("Loading key...")
# print("Key:", load_key())


def get_solution(url):
    # returns a json string of the solution

    # print("Sending request..\n", url)
    r = requests.get(url)

    # print("Response:", r)

    # save to json file
    result_file_name = r"src\server\trucks\truck_routing\mapbox\result.json"
    with open(result_file_name, 'w') as outfile:
        outfile.write(json.dumps(r.json()))

    return r.json()


def generate_problem(start, bins):
    """"
    start --> (longitude, latitude)
    bins --> list of (longitude, latitude)

    output: url to send to graphhopper
    """
    url = "https://api.mapbox.com/directions/v5/mapbox/driving/"
    url += str(start[0]) + "," + str(start[1]) + ";"
    for bin in bins:
        url += str(bin[0]) + "," + str(bin[1]) + ";"

    # remove last ;
    url = url[:-1]

    url += "?access_token=" + load_key()
    url += "&geometries=geojson"

    return url


def calculate_route_from_waypoints(start, bins):
    url = generate_problem(start, bins)
    solution = get_solution(url)
    return solution


if __name__ == "__main__":
    start = (13.406, 52.537)
    bins = [
        (9.999, 53.552),
        (11.57, 48.145)
    ]

    url = generate_problem(start, bins)
    solution = get_solution(url)
    print(solution)
