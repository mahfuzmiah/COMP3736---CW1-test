# cap at 118 for december and july
# 0 for august for holidays
# scatter plot amount on y month on x, school plotted
# heat map x is month y is school, colour is heat
# figures taken from gov website
import matplotlib.pyplot as plt
import numpy as np
from random import randint

# Define month names and colors for each school
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
colors = ['blue', 'orange', 'green', 'red', 'purple',
          'brown', 'pink', 'gray', 'olive', 'cyan']
markers = ['o', 's', '^', 'D', 'v', 'P', 'H', 'X', '*', '>']
schools = [f'School {i+1}' for i in range(10)]  # Names for each school


# Generate data with specific rules for December, July, and August
def generate_data(num_schools=10, num_months=12):
    data = np.array([[randint(0, 236) for _ in range(num_months)]
                    for _ in range(num_schools)])
    data[:, 6] = [randint(0, 118)
                  for _ in range(num_schools)]  # July (Month 7)
    data[:, 11] = [randint(0, 118)
                   for _ in range(num_schools)]  # December (Month 12)
    data[:, 7] = 0  # August (Month 8)
    return data


# Create the data
absences_data = generate_data()


def plot_scatter(data):
    num_months = data.shape[1]
    num_schools = data.shape[0]
    marker_size = 250
    marker_opacity = 0.8

    plt.figure(figsize=(14, 8))
    max_y_value = np.max(data) + 20

    for month in range(num_months):
        y_values = {}
        for school in range(num_schools):
            x = month + 1
            y = data[school, month]

            offset = 0
            for idx, key in enumerate(y_values.keys()):
                if abs(key - y) <= 10 and y != 0:
                    direction = -1 if (idx % 2 == 0) else 1
                    offset += direction * 0.05

            x_adjusted = x + offset
            y_values[y] = school

            plt.scatter(x_adjusted, y, marker=markers[school % len(markers)], edgecolors='white',
                        s=marker_size, color="black", alpha=marker_opacity,
                        label=f'School {school + 1}' if month == 0 else "")

    plt.xticks(ticks=np.arange(1, num_months + 1),
               labels=months, ha='center', fontsize=12)
    plt.xlim(0.5, num_months + 1)
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Number of Absences', fontsize=14)
    plt.ylim(0, max_y_value)
    plt.grid(True, linestyle='--', linewidth=0.5)

    plt.subplots_adjust(left=0.1, right=0.9)
    plt.legend(loc='center left', bbox_to_anchor=(0.99, 0.5),
               fontsize=12, markerscale=0.75)

    plt.title(
        'Scatter Plot of Pupil Absences Across Schools Over 12 Months', fontsize=16)
    plt.show()


# Heatmap function
def plot_heat(data):
    plt.figure(figsize=(12, 8))
    plt.imshow(data, aspect='auto', cmap='Hot')

    cbar = plt.colorbar()
    cbar.set_label('Number of Absences', rotation=270, labelpad=20)

    plt.xticks(ticks=np.arange(len(months)), labels=months,
               rotation=45, ha='right', fontsize=12)
    plt.yticks(ticks=np.arange(len(schools)), labels=schools, fontsize=12)

    plt.xlabel('Month', fontsize=14)
    plt.ylabel('School', fontsize=14)
    plt.title('Heatmap of Pupil Absences Across Schools Over 12 Months', fontsize=16)
    plt.tight_layout()
    plt.show()


# Run the heatmap plot
plot_heat(absences_data)

# Run the plot
plot_scatter(absences_data)
