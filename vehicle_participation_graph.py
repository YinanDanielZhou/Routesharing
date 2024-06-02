import numpy as np
import matplotlib.pyplot as plt
import random

PRIVACY_SENSITIVITY_RANGE = (0.1, 0.9)
NUM_OF_SERVER = 25
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
x = np.linspace(6e-4, 2.5e-3, 10)    # compensation c1
y = np.linspace(11.5, 13.75, 10)    # frequency fd
X, Y = np.meshgrid(x, y)   # X, Y are 2D array


Z = calculate_consumer_score(Y, X)
print(Z)
Z_percentage =calculateJoinPercentation(Z)
print(Z_percentage)


#### Labeled contour plot

# contour = plt.contour(X, Y, Z_percentage, colors='black')
# plt.clabel(contour, inline=True, fontsize=8, fmt='%1.2f')  # Inline labels with two decimal format
# plt.title('Vehicle Participation Rate')
# plt.xlabel('Compensation')
# plt.ylabel('Frequency of Data Sharing')
# plt.show()


#### Colored contour plot 

levels = np.linspace(0, 1, 11) # Specify contour levels
contourf = plt.contourf(X, Y, Z_percentage, levels=levels, cmap='viridis')  # Using a color map
plt.colorbar(contourf)  # Adds a color bar to the side of the plot
plt.title('Vehicle Participation Rate')
plt.xlabel('Compensation')
plt.ylabel('Frequency of Data Sharing')
plt.show()