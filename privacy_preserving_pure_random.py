from math import ceil
import random
import traceback
from tensorbay.geometry.polyline import Polyline2D

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


"""
Simulate the scenario where a car has p1 = (x1, y1) , p2 = (x2, y2) , p3 = (x3, y3) etc

The car send data points with timestamp to a server chosen at random

When the consumer collects the car data from all the servers, 
it need to sort them into the correct order in O(NlogN) time (sort by the timestamp)
"""


def calculate_similarity_score(car_id, total_server, compromised_server_list, num_of_samples, should_plot = False):
    x = []
    y = []
    with open(f"Car/Car_samples/car_{car_id}_data.txt", 'r') as fileIn:
        # Iterate over each line in the file
        count = 0
        for line in fileIn:
            elements = line.split(",")
            x.append(float(elements[1]))
            y.append(float(elements[2]))

            count += 1
            if count == num_of_samples:
                break


    x_original = np.array(x)
    y_original = np.array(y)

    x_reduced = np.array(x)
    y_reduced = np.array(y)

     # create a random list of compromised indexes
    # if 2 / 10 servers compromised, then randomly select 2 / 10 = 20 % (x, y) pairs (aka their indexes)
    compromised_percentage = len(compromised_server_list) / total_server
    compromised_sample_number = ceil(x_original.size * compromised_percentage)
    compromised_indexes = sorted(random.sample(range(x_original.size), compromised_sample_number))
    # print(compromised_indexes)
    
    # remove the not compromised points
    x_reduced = x_reduced[compromised_indexes]
    y_reduced = y_reduced[compromised_indexes]

    # Plotting the Graph
    
    if should_plot:
        plt.plot(x_original, y_original, '-b', label='original')
        plt.plot(x_reduced, y_reduced, '-r', label='reduced')
        plt.legend()

        plt.title(f"Car {car_id} history")
        plt.xlabel("Latitude E")
        plt.ylabel("Longitude N")

        plt.show()

    # calculating the ployline similarity
    polyline = np.stack((x_original, y_original), axis=-1)
    reduced_polyline = np.stack((x_reduced, y_reduced), axis=-1)
    try:
        similarity_score = Polyline2D.similarity(polyline, reduced_polyline) 
        print(f"car {car_id} has similarity score {round(similarity_score,3)}" )
        return similarity_score
    except Exception as e:
        # if the polyline is only one point (all x,y pair are the same), there will be a float division by zero error
        print(f"Error: in car {car_id} similarity score calculation: {e}")
        traceback.print_exc()
        raise e

total_server = 15
compromised_server_list = [2] # ints from [0, total_server)

# try:
#     print(calculate_similarity_score('2196', total_server, compromised_server_list, 100,  True))
# except Exception as e:
#     pass

# iterate through several cars and compute their average score
car_id_list = []
with open(f"Car/Car_samples/car_ids.txt", 'r') as fileIn:
    for car_id in fileIn:
         car_id_list.append(car_id.strip())

score_sum = 0
num_of_samples = float('inf')
success_count = 0
for i in range(len(car_id_list)):
    try:
        score_sum += calculate_similarity_score(car_id_list[i], total_server, compromised_server_list, num_of_samples)
        success_count += 1
    except Exception as e:
        print(f"Error: in car {car_id_list[i]} similarity score calculation: {e}")
print(f"Average Score: {round(score_sum / success_count, 3)}")