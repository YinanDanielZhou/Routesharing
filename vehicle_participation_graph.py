import numpy as np
import matplotlib.pyplot as plt
import random

# Define the function to plot
# def f(x, y):
#     return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

PRIVACY_SENSITIVITY_RANGE = (0.25, 0.75)

NUM_OF_SERVER = 15
NUM_OF_VEHICLES = 100

vehicle_privacy_sensitivity_list = [round(PRIVACY_SENSITIVITY_RANGE[0] + random.random() * (PRIVACY_SENSITIVITY_RANGE[1] - PRIVACY_SENSITIVITY_RANGE[0]), 3) for _ in range (NUM_OF_VEHICLES)]

print(vehicle_privacy_sensitivity_list[0])


def calculate_consumer_score(fd, c1):
    s = NUM_OF_SERVER
    loss = 1 - np.exp(-12.5 * fd / s) - np.exp(-0.1 * fd) - np.exp(-10 / s)
    privacy_score = (c1 * fd) / loss
    # print("privacy_score ", privacy_score)
    return privacy_score


def calculateJoinPercentation(Z):
    Z_percentage = np.zeros(Z.shape)

    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            # Count how many car's sensitivity requirement is met
            count_agree_to_join = np.sum(vehicle_privacy_sensitivity_list < Z[i, j])
            # Calculate the percentage
            percentage = count_agree_to_join / NUM_OF_VEHICLES
            # Store the percentage in Z_percentage
            Z_percentage[i, j] = percentage

    return Z_percentage

# Create grid and calculate Z values
x = np.linspace(1e-6, 1e-2, 10)    # compensation c1
y = np.linspace(7.1, 7.4, 10)    # frequency fd
X, Y = np.meshgrid(x, y)  


# print(calculateJoinPercentation(7.2, 5e-6))

# Z = calculateJoinPercentation(Y, X)

Z = calculate_consumer_score(Y, X)
print(Z)

Z_percentage =calculateJoinPercentation(Z)
print(Z_percentage)


plt.contour(X, Y, Z_percentage, colors='black')
plt.show()