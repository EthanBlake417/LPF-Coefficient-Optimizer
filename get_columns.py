import pandas as pd
from new_arrays_2 import goal_arr, start_arr
import numpy as np


print(len(start_arr), len(goal_arr))
# usuable factors of 2919 are 1,3,7,21
goal_sections = np.split(start_arr, 21)
print(goal_sections)
# print(pd.read_excel('coefficient_optomization_2.xlsx')["Ideal Wave (GOAL)"].dropna().tolist())