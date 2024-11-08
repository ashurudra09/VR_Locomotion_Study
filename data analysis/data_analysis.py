"""
Getting relevant information from excel sheet obtained from psytoolkit
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("PsyToolkitData_BRED_PROJECT_5_Nov/data.csv")
print(df.columns)

def convert_group(a):
    if a == 1:
        return "walking"
    if a == 2:
        return "joystick"
    return "invalid"

def convert_gender(a):
    if a == 1:
        return "woman"
    if a == 2:
        return "man"
    return "other"

def preprocessing_data():
    df["condition"] = df["psy_group"].apply(convert_group)
    df["gender"] = df["d_gender_1"].apply(convert_gender)

def lists_stats(walking, joystick, thing):
    # Calculate statistics for walking
    mean1 = np.mean(walking)
    median1 = np.median(walking)
    mode1 = stats.mode(walking, keepdims=True)[0][0]
    std_dev1 = np.std(walking)

    # Calculate outliers for walking using IQR
    q1_1, q3_1 = np.percentile(walking, [25, 75])
    iqr1 = q3_1 - q1_1
    lower_bound1 = q1_1 - 1.5 * iqr1
    upper_bound1 = q3_1 + 1.5 * iqr1
    outliers1 = [v for v in walking if v < lower_bound1 or v > upper_bound1]

    # Calculate statistics for joystick
    mean2 = np.mean(joystick)
    median2 = np.median(joystick)
    mode2 = stats.mode(joystick, keepdims=True)[0][0]
    std_dev2 = np.std(joystick)

    # Calculate outliers for joystick using IQR
    q1_2, q3_2 = np.percentile(joystick, [25, 75])
    iqr2 = q3_2 - q1_2
    lower_bound2 = q1_2 - 1.5 * iqr2
    upper_bound2 = q3_2 + 1.5 * iqr2
    outliers2 = [v for v in joystick if v < lower_bound2 or v > upper_bound2]

    # Print the statistics and outliers
    print(f"Walking Statistics for {thing}:")
    print(f"Mean: {mean1:.3f}")
    print(f"Median: {median1}")
    print(f"Mode: {mode1}")
    print(f"Standard Deviation: {std_dev1:.3f}")
    print(f"Outliers: {outliers1}\n")

    print(f"Joystick Statistics for {thing}:")
    print(f"Mean: {mean2:.3f}")
    print(f"Median: {median2}")
    print(f"Mode: {mode2}")
    print(f"Standard Deviation: {std_dev2:.3f}")
    print(f"Outliers: {outliers2}\n")

def lists_boxplot(walking, joystick, label):
    # Plot combined box plot
    plt.boxplot([walking, joystick], vert=True, labels=['Walking', 'Joystick'])
    plt.title(f"Box Plots of {label} for the two Conditions")
    plt.ylabel(label)
    plt.xlabel("Condition")
    plt.show()

def lists_histogram(walking, joystick, bins):

    plt.figure(figsize=(10, 6))
    plt.hist(walking, bins=bins, color="blue", alpha=0.5, edgecolor="black", label="Walking", align='left')
    plt.hist(joystick, bins=bins, color="red", alpha=0.5, edgecolor="black", label="Joystick", align='left')

    # Labels and title
    plt.xlabel("Number of Correct Objects")
    plt.ylabel("Frequency")
    plt.title("Histogram of Objects Correctly Placed for Each Condition")
    plt.xticks(range(5))  # Set x-ticks to be at each bin center for clarity
    plt.legend()
    plt.show()

def demographic_analysis():
    print(f"Gender of Participants:\t"
          f"Women: {df['gender'].value_counts()['woman']},"
          f" Men: {df['gender'].value_counts()['man']}")
    print(f"Age of participants:"
          f"\tMean: {df['d_age_1'].mean():.3f}, SD: {df['d_age_1'].std():.3f}")
    print(f"Number of participants in each Condition:\n"
          f"Walking: {df['condition'].value_counts()['walking']}\n"
          f"Joystick: {df['condition'].value_counts()['joystick']}")
    print(f"Time Taken for Completion of Entire Experiment:"
          f"\n\tMean: {df['TIME_total'].mean():.3f}, SD: {df['TIME_total'].std():.3f}\n")

def calc_ssq_scores(scores):
    nausea = [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1]
    oculomotor = [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
    disorientation = [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0]

    # Final score multiplier
    final_multiplier = 3.74

    total_scores = []
    for score in scores:
        # Calculate weighted sums for each category
        nausea_score = sum(s * w for s, w in zip(score, nausea))
        oculomotor_score = sum(s * w for s, w in zip(score, oculomotor))
        disorientation_score = sum(s * w for s, w in zip(score, disorientation))
        # Sum of all categories and apply final multiplier
        total_score = (nausea_score + oculomotor_score + disorientation_score) * final_multiplier
        total_scores.append(total_score)
    return total_scores

def ssq_analysis():
    v_question_columns = [col for col in df.columns if col.startswith('v_questions')]
    # Calculate the mean across 'v_questions' columns for each 'condition'
    ssq_walking, ssq_joystick = [], []
    for col in v_question_columns:
        ssq_walking.append(df[col][df['condition'] == 'walking'].tolist())
    for col in v_question_columns:
        ssq_joystick.append(df[col][df['condition'] == 'joystick'].tolist())
    walking_scores = calc_ssq_scores(ssq_walking)
    joystick_scores = calc_ssq_scores(ssq_joystick)
    lists_stats(walking_scores, joystick_scores, "Simulator Sickness")
    lists_boxplot(walking_scores, joystick_scores, "Simulator Sickness")

def presence_analysis():
    joystick_scores = df["presence_overall_1"][df["condition"] == 'joystick'].tolist()
    walking_scores = df["presence_overall_1"][df["condition"] == 'walking'].tolist()
    lists_stats(walking_scores, joystick_scores, "Presence")
    lists_boxplot(walking_scores, joystick_scores,
                  ["Overall Presence", "Condition"])

def task_performance():
    joystick_times = df["joystick_time_1"][df["condition"] == 'joystick'].tolist()
    walking_times = df["walking_time_1"][df["condition"] == 'walking'].tolist()
    lists_stats(walking_times, joystick_times,
                "Time for Task Completion")
    lists_boxplot(walking_times, joystick_times,"Time Taken (in s)")

    joystick_scores = df["joystick_score_1"][df["condition"] == 'joystick'].tolist()
    walking_scores = df["walking_score_1"][df["condition"] == 'walking'].tolist()
    lists_stats(walking_scores, joystick_scores,
                "Objects Correctly Placed")
    lists_histogram(walking_scores, joystick_scores,
                    [0, 1, 2, 3, 4, 5])

def task_feedback_analysis():
    ### It is in order Poorly to Clearly, 1 to 5.
    w_clarity = df["w_clarity_1"][df["condition"] == 'walking'].tolist()
    j_clarity = df["j_clarity_1"][df["condition"] == 'joystick'].tolist()
    lists_stats(w_clarity, j_clarity, "Clarity of Instructions")

    ### It is in order from difficult to easy, 1 to 5.
    w_difficulty = df["w_difficulty_1"][df["condition"] == 'walking'].tolist()
    j_difficulty = df["j_difficulty_1"][df["condition"] == 'joystick'].tolist()
    lists_stats(w_difficulty, j_difficulty, "Difficulty of Task")

    ### It is in order from difficult/uncomfortable to easy/confortable, 1 to 4.
    w_navigation = df["w_navigation_1"][df["condition"] == 'walking'].tolist()
    j_navigation = df["j_navigation_1"][df["condition"] == 'joystick'].tolist()
    lists_stats(w_navigation, j_navigation, "Ease of Navigation")

    ### Correlation between navigation and difficulty scores, for each condition:

    ### Analysis of Strategies used:
    w_strategy = df["w_strategy_1"][df["condition"] == 'walking'].tolist()
    j_strategy = df["j_strategy_1"][df["condition"] == 'joystick'].tolist()
    # print(w_strategy)
    # print(j_strategy)

preprocessing_data()
ssq_analysis()
# print(df["w_clarity_1"][df["condition"] == "walking"])
