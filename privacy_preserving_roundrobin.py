from tensorbay.geometry.polyline import Polyline2D

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def calculate_similarity_score(car_id, total_server, compromised_server_list, should_plot = False):
    x = []
    y = []
    with open(f"Car/Car_samples/car_{car_id}_data.txt", 'r') as fileIn:
            # Iterate over each line in the file
            # count = 0
            for line in fileIn:
                elements = line.split(",")
                x.append(float(elements[1]))
                y.append(float(elements[2]))
                # if count >= 1000:
                #     break
                # count += 1
                # raw_data.append((elements[1], elements[2]))

    x = np.array(x)
    y = np.array(y)

    x_reduced = x.copy()
    y_reduced = y.copy()

    for server_index in compromised_server_list:
        # set the compromised points to negatives
        x_reduced[server_index::total_server] = -x_reduced[server_index::total_server]
        y_reduced[server_index::total_server] = -y_reduced[server_index::total_server]

    # remove the positive points to keep the compromised points
    x_reduced = x_reduced[x_reduced < 0]  
    y_reduced = y_reduced[y_reduced < 0]

    # revert the compromised points back to positvie
    x_reduced = -x_reduced 
    y_reduced = -y_reduced

    # Plotting the Graph
    
    if should_plot:
        plt.plot(x, y, '-b', label='original')
        plt.plot(x_reduced, y_reduced, '-r', label='reduced')
        plt.legend()

        plt.title(f"Car {car_id} history")
        plt.xlabel("Latitude E")
        plt.ylabel("Longitude N")

        plt.show()

    # calculating the ployline similarity
    polyline = np.stack((x,y), axis=-1)
    reduced_polyline = np.stack((x_reduced, y_reduced), axis=-1)
    similarity_score = Polyline2D.similarity(polyline, reduced_polyline) 
    print(f"car {car_id} has similarity score {similarity_score}" )
    return similarity_score


total_server = 10
compromised_server_list = [2] # ints from [0, total_server)

# print(calculate_similarity_score('1381', total_server, compromised_server_list, True))


# # iterate through several cars and compute their average score
car_id_list = []
with open(f"Car/Car_samples/car_ids.txt", 'r') as fileIn:
    for car_id in fileIn:
         car_id_list.append(car_id.strip())

score_sum = 0
for i in range(len(car_id_list)):
    score_sum += calculate_similarity_score(car_id_list[i], total_server, compromised_server_list)
print(f"Average Score: {score_sum / len(car_id_list)}")