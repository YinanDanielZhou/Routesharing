import matplotlib.pyplot as plt
import numpy as np

x = np.array([0.066, 0.1, 0.133, 0.2])
y1 = np.array([0.675, 0.759, 0.768, 0.833])
#y2 = np.array([0.672, 0.733, 0.743, 0.807])
y3 = np.array([0.642, 0.712, 0.722, 0.784])
y4 = np.array([0.507, 0.603, 0.663, 0.731])
y5 = np.array([0.272, 0.304, 0.485, 0.521])

y5_err = np.array([[0, 0, (0.485 - 0.307), (0.521 - 0.312)],  # Min error
                   [0, 0, (0.663 - 0.485), (0.731 - 0.521)]]) # Max error

selected_x = x[-2:]
selected_y5 = y5[-2:]
selected_y5_err = y5_err[:, -2:]

lower_limit = selected_y5 - selected_y5_err[0]
upper_limit = selected_y5 + selected_y5_err[1]


plt.plot(x, y1, label='Round Robin')
#plt.plot(x, y2, label='Shift X')
plt.plot(x, y3, label='Secret Pattern')
plt.plot(x, y4, label='Pure Random')
plt.plot(x, y5, label='Pure Random (Splitting)', color='purple')

# Plot the error bars as separate dashed lines
for x, low, high in zip(selected_x, lower_limit, upper_limit):
    plt.plot([x, x], [low, high], 'k--', color='grey')
    plt.scatter([x, x], [low, high], color='purple', s=15)  # Dots at the ends of the error bars with size 20

plt.title('Privacy Preservation of Different Distribution Strategies')
plt.xlabel('Percentage of Compromised Servers')
plt.ylabel('Route Similarity Score')
plt.legend(fontsize='small')
plt.show()