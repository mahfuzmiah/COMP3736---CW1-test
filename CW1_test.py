# cap at 118 for december and july
# 0 for august for holidays
# scatter plot amount on y month on x, school plotted
# heat map x is month y is school, colour is heat
# figures taken from gov website

# add in a question asking how difficult they found it 1-5 + any comments

import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from random import randint
from datetime import datetime
import json  # Import JSON to convert data array to a string


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


def plot_scatter(data):
    num_months = data.shape[1]
    num_schools = data.shape[0]
    marker_size = 200
    marker_opacity = 0.65

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
                    offset += direction * 0.1

            x_adjusted = x + offset
            y_values[y] = school

            plt.scatter(x_adjusted, y, marker=markers[school % len(markers)], edgecolors='black',
                        s=marker_size, color=colors[school % len(
                            colors)], alpha=marker_opacity,
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
    plt.pause(1)  # Display plot briefly without blocking further code
    plt.close()  # Close the plot window after the pause

# Heatmap function


def plot_heat(data):
    plt.figure(figsize=(12, 8))
    plt.imshow(data, aspect='auto', cmap='plasma')

    cbar = plt.colorbar()
    cbar.set_label('Number of Absences', rotation=270, labelpad=20)

    plt.xticks(ticks=np.arange(len(months)), labels=months,
               rotation=45, ha='right', fontsize=12)
    plt.yticks(ticks=np.arange(len(schools)), labels=schools, fontsize=12)

    plt.xlabel('Month', fontsize=14)
    plt.ylabel('School', fontsize=14)
    plt.title('Heatmap of Pupil Absences Across Schools Over 12 Months', fontsize=16)
    plt.tight_layout()
    plt.pause(1)
    plt.close()


# Check if the user's answer is correct by identifying the school with the highest or lowest absences
def check_correctness(user_answer, data, month, question_type):
    if question_type == "highest":
        # Get indices of all schools with the max value for the month
        max_value = np.max(data[:, month])
        correct_schools_indices = np.where(data[:, month] == max_value)[0]
    elif question_type == "lowest":
        # Get indices of all schools with the min value for the month
        min_value = np.min(data[:, month])
        correct_schools_indices = np.where(data[:, month] == min_value)[0]

    # List of correct schools (1-indexed)
    correct_schools = [index + 1 for index in correct_schools_indices]
    # Absence value for any of the correct schools
    correct_absences = data[correct_schools_indices[0], month]

    try:
        user_school = int(user_answer)
        user_absences = data[user_school - 1,
                             month] if 1 <= user_school <= data.shape[0] else None
        is_correct = user_school in correct_schools
    except ValueError:
        user_school = None
        user_absences = None
        is_correct = False

    return is_correct, correct_schools, correct_absences, user_absences


# Main program to conduct trials, ask questions, and save responses
def main_program():
    user_number = input("What number user is this (1-10)? ")

    # Ensure valid user number
    while not user_number.isdigit() or not (1 <= int(user_number) <= 10):
        print("Please enter a valid user number between 1 and 10.")
        user_number = input("What number user is this (1-10)? ")

    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    trial_filename = "user_data.csv"
    feedback_filename = "user_feedback.csv"

    # Initialize trial data CSV file with headers if it doesn't exist
    with open(trial_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Session ID", "User Number", "Trial", "Month", "Chart Type", "Question Type",
                             "User Answer", "Correct School", "Correct Absences",
                             "User Absences", "Response Time", "Correct", "Generated Data"])

    # Initialize feedback data CSV file with headers if it doesn't exist
    with open(feedback_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(
                ["Session ID", "User Number", "Chart Type", "Confidence", "Rating", "Comments"])

    # Conduct trials based on user number
    if int(user_number) <= 5:
        # Run scatter plot trials first
        run_scatter_trials(trial_filename, user_number, session_id)

        # Collect feedback for scatter plot
        collect_feedback(feedback_filename, user_number,
                         "scatter plot", session_id)

        # Run heatmap trials next
        print("You have completed the first half of the evaluation with scatter plots.")
        print(
            "If you would like to continue with the heatmap evaluation, please press enter.")
        input()
        run_heat_trials(trial_filename, user_number, session_id)

        # Collect feedback for heatmap
        collect_feedback(feedback_filename, user_number, "heatmap", session_id)

    else:
        # Run heatmap trials first
        run_heat_trials(trial_filename, user_number, session_id)

        # Collect feedback for heatmap
        collect_feedback(feedback_filename, user_number, "heatmap", session_id)

        # Run scatter plot trials next
        print("You have completed the first half of the evaluation with heatmaps.")
        print("If you would like to continue with the scatter plot evaluation, please press enter.")
        input()
        run_scatter_trials(trial_filename, user_number, session_id)

        # Collect feedback for scatter plot
        collect_feedback(feedback_filename, user_number,
                         "scatter plot", session_id)

    print("Thank you for your participation and feedback!")


def run_scatter_trials(filename, user_number, session_id):
    for trial in range(10):
        print(f"\nTrial {trial + 1}")
        month = 7

        # Generate and display data
        while month == 7:
            month = randint(0, 11)

        # Ask questions
        responses = []

        question_type = "highest" if randint(0, 1) == 0 else "lowest"

        data = generate_data()
        # Convert data array to JSON string
        generated_data_str = json.dumps(data.tolist())

        plot_scatter(data)

        question = f"What is the school with the {question_type} value in {months[month]}?\n"  # nopep8
        start_time = time.time()
        answer = input(question)
        end_time = time.time()
        blank_screen()
        response_time = round(end_time - start_time, 2)

        is_correct, correct_school, correct_absences, user_absences = check_correctness(
            answer, data, month, question_type)

        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([session_id, user_number, trial + 1, months[month], "scatter", question_type, answer, f"School {correct_school}", correct_absences, user_absences, response_time, "Correct" if is_correct else "Wrong", generated_data_str])  # nopep8


def run_heat_trials(filename, user_number, session_id):
    for trial in range(10):
        print(f"\nTrial {trial + 1}")
        month = 7

        # Generate and display data
        while month == 7:
            month = randint(0, 11)

        # Ask questions
        responses = []

        question_type = "highest" if randint(0, 1) == 0 else "lowest"

        data = generate_data()
        # Convert data array to JSON string
        generated_data_str = json.dumps(data.tolist())

        plot_heat(data)

        question = f"What is the school with the {question_type} value in {months[month]}?\n"  # nopep8
        start_time = time.time()
        answer = input(question)
        end_time = time.time()
        response_time = round(end_time - start_time, 2)

        is_correct, correct_school, correct_absences, user_absences = check_correctness(
            answer, data, month, question_type)

        # Save trial data
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([session_id, user_number, trial + 1, months[month], "heat", question_type,
                             answer, f"School {correct_school}", correct_absences, user_absences, response_time, "Correct" if is_correct else "Wrong", generated_data_str])  # nopep8


def collect_feedback(filename, user_number, chart_type, session_id):
    """Collects feedback from the user for a specific chart type and saves it to the feedback CSV."""
    print(f"\nPlease provide feedback for the {chart_type} charts: \n")
    confidence = input(
        f"On a scale of 1-10, how would you rate your confidence of reading {chart_type}s before you took this test? ")
    rating = input(
        f"On a scale of 1-10, how would you rate the {chart_type}s for clarity? ")
    comments = input(f"Please provide any additional comments on the {chart_type}s: ")  # nopep8

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([session_id, user_number, chart_type,
                        confidence, rating, comments])


def blank_screen(duration=1):
    plt.figure(figsize=(12, 8))
    plt.axis('off')  # Hide axes to simulate a blank screen
    # Pause for the specified duration to keep the blank screen visible
    plt.pause(duration)
    plt.close()  # Close the blank screen after the pause


# Run the main program
main_program()


# program made by Mohammed Mahfuz Miah Email: sc22mm@leeds.ac.uk
