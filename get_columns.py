import pandas as pd
from new_arrays import goal_arr, start_arr
import numpy as np


print(len(start_arr), len(goal_arr))
print(6021/10)
goal_sections = np.split(start_arr, 9)
print(goal_sections)
# print(pd.read_excel('coefficient_optomization.xlsx')['Pure Scaled Sine Wave (GOAL)'].dropna().tolist())