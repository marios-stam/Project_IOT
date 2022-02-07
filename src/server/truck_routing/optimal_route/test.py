# https://graphhopper.com/api/1/vrp?key=<your_key>
from classes import *
import requests
import os
import waypoints
print("Current working directory:", os.getcwd())


def load_key():  # load key from .txt file
    with open(r"src\server\truck_routing\optimal_route\api_key.txt", "r") as key_file:
        key = key_file.read()
    return key


def send_request(problem_file='problem.json'):
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}
    r = requests.post(url, data=open(problem_file, 'rb'), headers=headers)
    print(r)
    # save to json file
    with open('result.json', 'w') as outfile:
        outfile.write(json.dumps(r.json()))


url = "https://graphhopper.com/api/1/vrp?key=" + load_key()
print("URL:", url)


def generate_test_problem():
    print("Testing classes.")
    veh = Vehicle("fortigo", "truck_loc", 13.406, 52.537)

    serv1 = Service("1", "test1", "test_loc", 9.999, 53.552)

    serv2 = Service("2", "test2", "test_loc2", 11.57, 48.145)

    prob = Problem()
    prob.add_vehicle(veh)

    prob.add_service(serv1)
    prob.add_service(serv2)

    json_str = prob.get_json()

    # save string to file
    with open('problem.json', 'w') as outfile:
        outfile.write(json_str)

    with open('problem.json') as f:
        data = json.load(f)

    print("opa mlka")

    print(type(data))
    print(data)

    return data


def generate_problem(truck_pos, bins_to_collect):
    """
       truck_pos: (longitude, latitude)
       bins_to_collect: list of (longitude, latitude)
   """
    prob = Problem()

    veh = Vehicle("fortigo", "truck_loc", truck_pos[0], truck_pos[1])
    prob.add_vehicle(veh)

    for i, bin in enumerate(bins_to_collect):
        ii = str(i)
        serv = Service(ii, "test" + ii, "test_loc"+ii, bin[0], bin[1])
        prob.add_service(serv)

    json_str = prob.get_json()

    # save string to file
    with open('problem.json', 'w') as outfile:
        outfile.write(json_str)

    with open('problem.json') as f:  # TODO remove this extra
        data = json.load(f)

    print("opa mlka")

    print(type(data))
    print(data)

    return data


# data_test = generate_test_problem()

if __name__ == "__main__":
    truck_pos = (13.406, 52.537)
    bins_to_collect = [(9.999, 53.552), (11.57, 48.145)]
    generate_problem(truck_pos, bins_to_collect)

    send_request()

    waypoints.extract_waypoints_from_result()
