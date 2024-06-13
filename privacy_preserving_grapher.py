import matplotlib.pyplot as plt
import numpy as np

x = np.array([0.066, 0.1, 0.133, 0.2])
y1 = np.array([0.675, 0.759, 0.768, 0.833])
y2 = np.array([0.672, 0.733, 0.743, 0.807])
y3 = np.array([0.642, 0.712, 0.722, 0.784])
y4 = np.array([0.507, 0.603, 0.663, 0.731])
y5 = np.array([0.272, 0.304, 0.485, 0.521])

plt.plot(x, y1, label='Round Robin')
plt.plot(x, y2, label='Shift X')
plt.plot(x, y3, label='Secret Pattern')
plt.plot(x, y4, label='Pure Random')
plt.plot(x, y5, label='Pure Random (Segregate)')

plt.title('Privacy preserving ability of different distribution strategies')

plt.xlabel('Percentage of servers compromised')
plt.ylabel('Similarity Score between the compromised and the ground truth.')
plt.show()