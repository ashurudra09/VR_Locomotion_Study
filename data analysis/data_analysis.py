"""
Getting relevant information from excel sheet obtained from psytoolkit
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("PsyToolkitData_BRED_PROJECT_5_Nov/data.csv")
# print(df.columns)

def convert_group(a):
    if a == 1:
        return "walking"
    elif a == 2:
        return "joystick"
    else:
        return "invalid"

def convert_gender(a):
    if a == 1:
        return "woman"
    elif a == 2:
        return "man"
    else:
        return "other"

df["condition"] = df["psy_group"].apply(convert_group)
df["gender"] = df["d_gender_1"].apply(convert_gender)

print("Number of participants in each", df["condition"].value_counts())

print("Average time taken for completion of entire experiment:", df["TIME_total"].mean())

print(df["gender"].value_counts())

print("Average age:", df["d_age_1"].mean())

def average_ssq_scores():
    nausea = [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1]
    oculomotor = [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
    disorientation = [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0]

    v_question_columns = [col for col in df.columns if col.startswith('v_questions')]
    # Calculate the mean across 'v_questions' columns for each 'condition'
    grouped_means = df.groupby('condition')[v_question_columns].mean()
    # Convert each row of means to a list for each unique 'condition' value
    result = {group: row.tolist() for group, row in grouped_means.iterrows()}
    # print(result)

    # Final score multiplier
    final_multiplier = 3.74
    # Calculate the final scores for each 'condition'
    final_scores = {}
    for group, scores in result.items():
        # Calculate weighted sums for each category
        nausea_score = sum(s * w for s, w in zip(scores, nausea))
        oculomotor_score = sum(s * w for s, w in zip(scores, oculomotor))
        disorientation_score = sum(s * w for s, w in zip(scores, disorientation))
        # Sum of all categories and apply final multiplier
        total_score = (nausea_score + oculomotor_score + disorientation_score) * final_multiplier
        final_scores[group] = total_score

    print(final_scores)

average_ssq_scores()
