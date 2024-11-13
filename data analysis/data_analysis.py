"""
Getting relevant information from Excel sheet obtained from PsyToolkit
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg
from scipy import stats

df = pd.read_csv("PsyToolkitData_BRED_PROJECT_11_Nov/data.csv")
print(df.columns)

df.loc[df["walking_time_1"].isna() & (df["psy_group"] == 1), "psy_group"] = 2
df.loc[df["joystick_time_1"].isna() & (df["psy_group"] == 2), "psy_group"] = 1
# print(df["walking_time_1"][df["psy_group"] == 1])

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

def list_stats(l, thing, condition=""):
    # Calculate statistics for walking
    mean = np.mean(l)
    median = np.median(l)
    mode = stats.mode(l, keepdims=True)[0][0]
    std_dev = np.std(l)

    # Calculate outliers for walking using IQR
    q1, q3 = np.percentile(l, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers1 = [v for v in l if v < lower_bound or v > upper_bound]

    print(f"{condition}Statistics for {thing}:")
    print(f"Mean: {mean:.3f}")
    print(f"Median: {median}")
    print(f"Mode: {mode}")
    print(f"Standard Deviation: {std_dev:.3f}")
    print(f"Outliers: {outliers1}\n")

def lists_stats_wrapper(walking, joystick, thing):
    list_stats(walking, thing, "Walking ")
    list_stats(joystick, thing, "Joystick ")

def lists_boxplot(walking, joystick, label):
    # Plot combined box plot
    plt.boxplot([walking, joystick], vert=True, labels=['Walking', 'Joystick'])
    plt.title(f"Box Plots of {label} for each Condition")
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
          f"\tWalking: {df['condition'].value_counts()['walking']}\n"
          f"\tJoystick: {df['condition'].value_counts()['joystick']}")
    print(f"Prior Experience in VR among Participants:\n"
          f"\tMean: {df['d_vr_experience_1'].mean():.3f}, SD: {df['d_vr_experience_1'].std():.3f}")
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
    lists_stats_wrapper(walking_scores, joystick_scores, "Simulator Sickness")
    lists_boxplot(walking_scores, joystick_scores, "Simulator Sickness")

def presence_analysis():
    joystick_scores = df["presence_overall_1"][df["condition"] == 'joystick'].tolist()
    walking_scores = df["presence_overall_1"][df["condition"] == 'walking'].tolist()
    lists_stats_wrapper(walking_scores, joystick_scores, "Presence")
    lists_boxplot(walking_scores, joystick_scores,
                  "Overall Presence")

def task_performance():
    joystick_times = df["joystick_time_1"][df["condition"] == 'joystick'].tolist()
    walking_times = df["walking_time_1"][df["condition"] == 'walking'].tolist()
    lists_stats_wrapper(walking_times, joystick_times,
                "Time for Task Completion")
    lists_boxplot(walking_times, joystick_times,"Time Taken (in s)")

    joystick_scores = df["joystick_score_1"][df["condition"] == 'joystick'].tolist()
    walking_scores = df["walking_score_1"][df["condition"] == 'walking'].tolist()
    lists_stats_wrapper(walking_scores, joystick_scores,
                "Objects Correctly Placed")
    lists_histogram(walking_scores, joystick_scores,
                    [0, 1, 2, 3, 4, 5])

def task_feedback_analysis():
    ### It is in order Poorly to Clearly, 1 to 5.
    w_clarity = df["w_clarity_1"][df["condition"] == 'walking'].tolist()
    j_clarity = df["j_clarity_1"][df["condition"] == 'joystick'].tolist()
    lists_stats_wrapper(w_clarity, j_clarity, "Clarity of Instructions")

    ### It is in order from difficult to easy, 1 to 5.
    w_difficulty = df["w_difficulty_1"][df["condition"] == 'walking'].tolist()
    j_difficulty = df["j_difficulty_1"][df["condition"] == 'joystick'].tolist()
    lists_stats_wrapper(w_difficulty, j_difficulty, "Difficulty of Task")

    ### It is in order from difficult/uncomfortable to easy/confortable, 1 to 4.
    w_navigation = df["w_navigation_1"][df["condition"] == 'walking'].tolist()
    j_navigation = df["j_navigation_1"][df["condition"] == 'joystick'].tolist()
    lists_stats_wrapper(w_navigation, j_navigation, "Ease of Navigation")

    ### Correlation between navigation and difficulty scores, for each condition:

    ### Analysis of Strategies used:
    w_strategy = df["w_strategy_1"][df["condition"] == 'walking'].tolist()
    j_strategy = df["j_strategy_1"][df["condition"] == 'joystick'].tolist()
    # print(w_strategy)
    # print(j_strategy)

def cba_reliability(construct):
    constructs = {
        "Presence": {
            "joystick": df[['p_q1_1', 'p_q2_1', 'p_q3_1',
                            'p_q4_1', 'p_q5_1', 'p_q6_1',
                            'p_q7_1', 'p_q8_1', 'p_q9_1',
                            'p_q10_1', 'p_q11_1']][df['condition'] == 'joystick'],
            "walking": df[['p_q1_1', 'p_q2_1', 'p_q3_1',
                           'p_q4_1', 'p_q5_1', 'p_q6_1',
                           'p_q7_1', 'p_q8_1', 'p_q9_1',
                           'p_q10_1', 'p_q11_1']][df['condition'] == 'walking']
        },
        "Simulator Sickness": {
            "joystick": df[['v_questions_1', 'v_questions_2', 'v_questions_3',
                            'v_questions_4', 'v_questions_5', 'v_questions_6',
                            'v_questions_7', 'v_questions_8', 'v_questions_9',
                            'v_questions_10', 'v_questions_11', 'v_questions_12',
                            'v_questions_13', 'v_questions_14', 'v_questions_15'
                            ]][df['condition'] == 'joystick'],
            "walking": df[['v_questions_1', 'v_questions_2', 'v_questions_3',
                           'v_questions_4', 'v_questions_5', 'v_questions_6',
                           'v_questions_7', 'v_questions_8', 'v_questions_9',
                           'v_questions_10', 'v_questions_11', 'v_questions_12',
                           'v_questions_13', 'v_questions_14', 'v_questions_15'
                           ]][df['condition'] == 'walking']  },
    }
    df_j = constructs[construct]["joystick"]
    df_w = constructs[construct]["walking"]

    print(f"Reliability Analysis for {construct}:")
    print(f"\tCronbach Alpha for Joystick Condition: {pg.cronbach_alpha(df_j)[0]:.3f}\n"
          f"\tCronbach Alpha for Walking Condition: {pg.cronbach_alpha(df_w)[0]:.3f}\n")

def reliability_analysis():
    cba_reliability("Simulator Sickness")
    cba_reliability("Presence")

### TRYING TO FIGURE OUT HOW TO CALCULATE P-VALUE
preprocessing_data()
# ssq_analysis()


v_question_columns = [col for col in df.columns if col.startswith('v_questions')]
# Calculate the mean across 'v_questions' columns for each 'condition'
ssq_walking, ssq_joystick = [], []
for col in v_question_columns:
    ssq_walking.append(df[col][df['condition'] == 'walking'].tolist())
for col in v_question_columns:
    ssq_joystick.append(df[col][df['condition'] == 'joystick'].tolist())
walking_scores = calc_ssq_scores(ssq_walking)
joystick_scores = calc_ssq_scores(ssq_joystick)

_, pvalue = stats.shapiro(walking_scores)
print(f"Normality of walking SSQ scores: {pvalue}")
_, pvalue = stats.shapiro(joystick_scores)
print(f"Normality of joystick SSQ scores: {pvalue}")

_, pvalue = stats.mannwhitneyu(walking_scores, joystick_scores)
print(f"PValue (ttest): {pvalue}")
