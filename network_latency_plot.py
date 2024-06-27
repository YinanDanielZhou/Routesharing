import pandas as pd
import matplotlib.pyplot as plt

# Hardcoded data
data = {
    'Number of Samples': [5, 50, 100, 150, 300, 600, 1200],
    '5 Servers': [0.2694, 0.2958, 0.2915, 0.2938, 0.3015, 0.3127, 0.3343],
    '10 Servers': [0.272, 0.2746, 0.2899, 0.2936, 0.3008, 0.3093, 0.3247],
    '15 Servers': [0.2735, 0.2772, 0.2768, 0.2949, 0.2998, 0.3085, 0.3219],
    '20 Servers': [0.275, 0.2777, 0.2756, 0.2804, 0.2981, 0.3036, 0.3129]
}

# Convert dictionary to DataFrame
df = pd.DataFrame(data)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(df['Number of Samples'], df['5 Servers'], label='5 Servers')
plt.plot(df['Number of Samples'], df['10 Servers'], label='10 Servers')
plt.plot(df['Number of Samples'], df['15 Servers'], label='15 Servers')
plt.plot(df['Number of Samples'], df['20 Servers'], label='20 Servers')
plt.xlabel('Number of Samples')
plt.ylabel('Read Latency (s)')
plt.title('Read Latency vs Number of Samples for Different Server Counts')
plt.legend()
plt.grid(True)
plt.show()

