import pandas as pd 
import numpy as np
import scipy
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split 

df = pd.read_csv("stroop_results.csv")
print(df.head())
reaction_times = df["reaction_time"]
mean = float(np.mean(reaction_times))
median = float(np.median(reaction_times))
print(f"Mean: {mean:.3f}, Median: {median:.3f}") 

df_true = df[df["is_correct"]]
percentage_accuracy = len(df_true) / len(df) * 100
print(f"The accuracy percentage is {percentage_accuracy:.3f}%.") 

congruent_indices = df[df["word"].str.lower() == df["color"]].index
df_congruent = df.iloc[list(congruent_indices)] 
congruent_reaction_times = df_congruent["reaction_time"] 

df_incongruent = df[~df.index.isin(df_congruent.index)]
incongruent_reaction_times = df_incongruent["reaction_time"]

cong_mean = float(np.mean(congruent_reaction_times)) 
incong_mean = float(np.mean(incongruent_reaction_times)) 
incong_mean > cong_mean 

cong_median = float(np.median(congruent_reaction_times)) 
incong_median = float(np.median(incongruent_reaction_times)) 
incong_median > cong_median

from scipy.stats import ttest_ind
t_stat, p_value = ttest_ind(list(incongruent_reaction_times), list(congruent_reaction_times))
print(f"T-statistic: {float(t_stat)}, P-value: {float(p_value)}")

is_correct = df["is_correct"]

X = df["reaction_time"].values.
y = df["is_correct"].values








