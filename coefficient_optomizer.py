import random
import threading
import time
import numpy as np
from new_arrays import goal_arr, start_arr
import matplotlib.pyplot as plt
import multiprocessing
import winsound
import logging


# Now we are trying to match the original to just a regular sine wave
# This means I need to create a new goal arr in file arrays.py

def program(thread_number, best_sum, PreFilter_Gain, HPF_G1, LPF_G1, Through_Gain1, HPF_G2, LPF_G2, Through_Gain2, PreFilter_TC, HPF_TC1, LPF_TC1, HPF_TC2, LPF_TC2):
    logging.basicConfig(level=logging.INFO,
                        filename=f"Logging/log_{thread_number}.log",
                        filemode="w",
                        format="%(asctime)s - %(levelname)s - %(message)s")

    coeff_arr = np.array([PreFilter_Gain, HPF_G1, LPF_G1, Through_Gain1, HPF_G2, LPF_G2, Through_Gain2, PreFilter_TC, HPF_TC1, LPF_TC1, HPF_TC2, LPF_TC2])
    factor = [.01, .001, .0001, .00001, .000001, .0000001]

    counter = 0
    every_one_hundredth = 0
    while True:
        best_sums_printed = 0
        down = False
        random_ordering = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11]
        random.shuffle(random_ordering)
        # print(random_ordering)
        for i in random_ordering:
            for element in factor:
                down = False if down else True
                direction = 'down' if down else 'up'
                direction_change = 0
                while direction_change < 2:
                    if direction == 'up':
                        coeff_arr[i] += element
                    elif direction == 'down':
                        coeff_arr[i] -= element

                    cur_sum, final_sum_arr = get_sum_arr(*coeff_arr, method=thread_number)
                    if cur_sum < best_sum:
                        counter = 0
                        best_sums_printed += 1
                        every_one_hundredth += 1
                        best_sum = cur_sum
                        if every_one_hundredth >= 100:
                            every_one_hundredth = 0
                            logging.info(
                                f'{thread_number}, {best_sum}\n{coeff_arr[0]}, {coeff_arr[1]}, {coeff_arr[2]}, {coeff_arr[3]}, {coeff_arr[4]}, {coeff_arr[5]}, {coeff_arr[6]}, {coeff_arr[7]}, {coeff_arr[8]}, {coeff_arr[9]}, {coeff_arr[10]}, {coeff_arr[11]}')
                    else:
                        direction_change += 1
                        if direction == 'up':
                            coeff_arr[i] -= element
                            direction = 'down'
                        else:
                            coeff_arr[i] += element
                            direction = 'up'
        if best_sums_printed == 0:
            counter += 1
        if counter >= 4:
            break
    with open('best_solutions.txt', 'a') as f:
        f.write(
            f'{thread_number}, {best_sum}\n{coeff_arr[0]}, {coeff_arr[1]}, {coeff_arr[2]}, {coeff_arr[3]}, {coeff_arr[4]}, {coeff_arr[5]}, {coeff_arr[6]}, {coeff_arr[7]}, {coeff_arr[8]}, {coeff_arr[9]}, {coeff_arr[10]},{ coeff_arr[11]}\n')
    logging.info(f"Process {thread_number} Done")
    logging.info(
        f'{thread_number}, {best_sum}\n{coeff_arr[0]}, {coeff_arr[1]}, {coeff_arr[2]}, {coeff_arr[3]}, {coeff_arr[4]}, {coeff_arr[5]}, {coeff_arr[6]}, {coeff_arr[7]}, {coeff_arr[8]}, {coeff_arr[9]}, {coeff_arr[10]}, {coeff_arr[11]}')
    # logging.info(f"Starting Process {thread_number} Over with New Coefficients")
    # winsound.Beep(440, 2500)
    print(f"Process {thread_number} Done")
    # best_sum, coeff_arr = fresh_coefficients()
    # print(f"Starting Process {thread_number} Over with New Coefficients")
    # program(thread_number, best_sum, *coeff_arr)


def main():
    # this section gets us a decent random starting point
    # this time using squared instead of abs
    for i in range(3):
        # if i == 0:
        #     og_sum = 70000
        # elif i == 1:
        #     og_sum = 70000
        # else:
        #     og_sum = 2500000
        og_sum = 999999
        cur_sum = float('inf')
        coeff_arr = None
        while og_sum < cur_sum:
            coeff_arr = [round(random.uniform(0, 1), 4) for _ in range(12)]
            # coeff_arr[6] = .0006
            cur_sum, cur_sum_arr = get_sum_arr(*coeff_arr, method=i)
        if i == 0:
            coeff_arr = [2.6388674000000942, -0.20393999999999995, 23.766464400001453, 0.21732629999999795, -1.198259999999985, 0.9975551999999853, -0.18376879999999557, 0.418, 0.017385899999998476, 0.01739379999999823, 0.01609789999999864, 0.01630079999999897]
        elif i == 1:
            coeff_arr = [0.6185585999999866, 4.615245100000006, 11.834540599999919, -5.140384800000144, -19.45480640000046, 19.581943600000226, 0.08311400000000053, 0.5368, 0.2105836999999988, 0.009946799999999223, 0.020598699999999966, 1.0040097000000063]
        elif i == 2:
            coeff_arr = [0.7040968999999984, -1.45716719999998, 1.2220224000000208, -0.08416110000000022, -0.4941555000000284, 80.04012220000415, 0.4966880999999722, 0.4743, 0.015734899999999254, 0.015680499999998737, 0.014422299999998167, 0.014143899999998585]
        # if i == 0:
        #     coeff_arr = [0.43110840000000067, -0.09648450000000017, 26.467515200001362, 0.08402379999999943, -16.573753799999746, 7.747459899999862, 6.52795409999987, 0.9722, -0.001114400000000309, 0.011078199999999521, 0.01221449999999957, 0.013741199999999567]
        print(f"Process {i} beginning!")
        # limits = True if i % 2 == 0 else False
        multiprocessing.Process(target=program,
                                args=(i, og_sum, *coeff_arr)).start()


def comparison_method(method, final_sum_arr, num_split=9):
    attempt_sections = np.split(final_sum_arr, num_split)
    goal_sections = np.split(goal_arr, num_split)
    summation = None
    if method == 0:
        sums = np.array(
            [sum(abs(goal_sections[i] - attempt_sections[i])) for i in
             range(num_split)])
        summation = sum(sums[0:3])
    elif method == 1:
        sums = np.array(
            [sum(abs(goal_sections[i] - attempt_sections[i])) for i in
             range(num_split)])
        summation = sum(sums[0:6])
    elif method == 2:
        sums = np.array(
            [sum(abs(goal_sections[i] - attempt_sections[i])) for i in
             range(num_split)])
        summation = sum(sums)
    return summation


def get_sum_arr(PreFilter_Gain, HPF_G1, LPF_G1, Through_Gain1, HPF_G2, LPF_G2, Through_Gain2, PreFilter_TC, HPF_TC1, LPF_TC1, HPF_TC2, LPF_TC2, method=0):
    # goal array is column E, start array is column B
    PreFilter_HPF = pass_filter(hpf=True, input_arr=start_arr, TC=PreFilter_TC, G=PreFilter_Gain)

    HPF_1 = pass_filter(hpf=True, input_arr=PreFilter_HPF, TC=HPF_TC1, G=HPF_G1)
    LPF_1 = pass_filter(hpf=False, input_arr=PreFilter_HPF, TC=LPF_TC1, G=LPF_G1)
    sum_1 = Through_Gain1 * PreFilter_HPF + HPF_1 + LPF_1

    HPF_2 = pass_filter(hpf=True, input_arr=sum_1, TC=HPF_TC2, G=HPF_G2)
    LPF_2 = pass_filter(hpf=False, input_arr=sum_1, TC=LPF_TC2, G=LPF_G2)
    sum_out = Through_Gain2 * sum_1 + HPF_2 + LPF_2

    summation = comparison_method(method=method, final_sum_arr=sum_out,
                                  num_split=9)
    return summation, sum_out


def pass_filter(hpf, input_arr, TC, G):
    hpf_arr = np.zeros(len(input_arr))
    lpf_arr = np.zeros(len(input_arr))
    for i in range(1, len(input_arr)):
        hpf_arr[i] = G * input_arr[i - 1] - lpf_arr[i - 1]
        lpf_arr[i] = TC * hpf_arr[i] + lpf_arr[i - 1]
    if hpf:
        return hpf_arr
    return lpf_arr


if __name__ == '__main__':
    main()
