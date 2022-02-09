import requests
import os

try:
    from classes import *
    from waypoints import extract_waypoints_from_result
except:
    from .classes import *
    from .waypoints import extract_waypoints_from_result


# print("Current working directory:", os.getcwd())
problem_file_name = r"src\server\trucks\truck_routing\trav_salesman_problem\problem.json"
result_file_name = r"src\server\trucks\truck_routing\trav_salesman_problem\result.json"
final_result_file_name = r"src\server\trucks\truck_routing\trav_salesman_problem\final_result.json"
api_key_file_name = r"src\server\trucks\truck_routing\trav_salesman_problem\api_key.txt"


def load_key():  # load key from .txt file
    with open(api_key_file_name, "r") as key_file:
        key = key_file.read()
    return key


def send_request(problem_file=problem_file_name):
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}
    r = requests.post(url, data=open(problem_file, 'rb'), headers=headers)
    # print(r)
    # save to json file
    with open(result_file_name, 'w') as outfile:
        outfile.write(json.dumps(r.json()))


url = "https://graphhopper.com/api/1/vrp?key=" + load_key()
# print("URL:", url)


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
    with open(problem_file_name, 'w') as outfile:
        outfile.write(json_str)

    with open(problem_file_name) as f:
        data = json.load(f)

    print("opa mlka")

    print(type(data))
    print(data)

    return data


def generate_problem(trucks, bins_to_collect):
    """
        trucks: list of (truck_id,longitude, latitude)
        bins_to_collect: list of (longitude, latitude)
   """
    prob = Problem()

    for i, truck in enumerate(trucks):
        truck_id = truck[0]
        truck_long = truck[1]
        truck_lat = truck[2]
        veh = Vehicle(truck_id, "truck_loc"+str(i), truck_long, truck_lat)

        prob.add_vehicle(veh)

    for i, bin in enumerate(bins_to_collect):
        ii = str(i)
        serv = Service(ii, "test" + ii, "test_loc"+ii, bin[0], bin[1])
        prob.add_service(serv)

    json_str = prob.get_json()

    # save string to file
    with open(problem_file_name, 'w') as outfile:
        outfile.write(json_str)

    with open(problem_file_name) as f:  # TODO remove this extra
        data = json.load(f)

    # print(type(data))
    # print(data)

    return data


def get_waypoints_for_each_truck(trucks, bins_pos):
    """
    trucks: list of (truck_id,longitude, latitude)
    bins_pos: list of (longitude, latitude)
    """
    generate_problem(trucks, bins_pos)
    send_request()
    routes = extract_waypoints_from_result()
    return routes

# data_test = generate_test_problem()


if __name__ == "__main__":
    trucks = [("truck_id1", 9.997, 53.551), ("truck_id2", 11.57, 48.144)]
    bins_to_collect = [(9.999, 53.552), (9.998, 53.553),
                       (11.57, 48.145), (11.56, 48.146)]

    trucks_tasks = get_waypoints_for_each_truck(trucks, bins_to_collect)

    print("==========FINAL RESULT==========")
    print(json.dumps(trucks_tasks))
    # save to json file
    with open(final_result_file_name, 'w') as outfile:
        outfile.write(json.dumps(trucks_tasks))

    # extract_waypoints_from_result()
