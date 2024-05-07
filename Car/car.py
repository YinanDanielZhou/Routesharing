from ast import Constant
import numpy as np
import requests

COORDINATOR_URL = "http://127.0.0.1:5000"
PRIVACY_SENSITIVITY = 0.002
PAYMENT_METHOD = "Public Key ...."

def get_consumers_info():
    url_suffix = "/consumers"
    response = requests.get(COORDINATOR_URL+url_suffix)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response content (JSON data)
        # print("Response content:")    
        # print(response.json())  # Parse JSON response
        return response.json()['consumers']

    else:
        print("Request failed with status code:", response.status_code)
        print(response.json())
        return []



def filter_consumers(all_consumers):
    def agree_to_join_consumer(s, fd, c1):
        loss = 1 - np.exp(-12.5 * fd / s) - np.exp(-0.1 * fd) - np.exp(-10 / s)
        privacy_score = (c1 * fd) / loss
        print("privacy_score ", privacy_score)
        return privacy_score > PRIVACY_SENSITIVITY

    result = []
    # id: consumer id
    # c1: consumer compensation
    # fd: consumer frequency
    # s:  consumer number of servers
    for (id, c1, fd, s) in all_consumers:
        print("Decision on consumer ", id)
        if agree_to_join_consumer(s, fd, c1):
            result.append(id)

    return result

def register_at_coordinator(consumer_id):
    url_suffix = "/register/car"
    data = {
        "consumer_id": consumer_id,
        "payment_method" : PAYMENT_METHOD
    }
    response = requests.post(COORDINATOR_URL+url_suffix, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 201:
        # Print the response content (JSON data)
        # print("Response content:")
        # print(response.json())  # Parse JSON response
        return (response.json()["Assigned_ID"], response.json()["paired_servers"])
    else:
        print("Request failed with status code:", response.status_code)
        print(response.json())



def initialize(consumer_server_lookup):
    chosen_consumers = filter_consumers(get_consumers_info())

    print(chosen_consumers)

    for consumer_id in chosen_consumers:
        car_id, servers = register_at_coordinator(consumer_id)
        consumer_server_lookup[car_id] = (consumer_id, servers)
    
    print(consumer_server_lookup)