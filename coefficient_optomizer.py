import random
import threading
import time
import numpy as np
from arrays import goal_arr, start_arr
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

                    cur_sum, final_sum_arr = get_sum_arr(*coeff_arr, method=0)
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
    with open('readme.txt', 'a') as f:
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
    for i in range(1):
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
            cur_sum, cur_sum_arr = get_sum_arr(*coeff_arr, method=0)
        # if i == 0:
        #     coeff_arr = [1.1041402299999334, 0.5922905199999743, 0.20565499000002624, 0.10039526000000747, 105.76726719001645, 12.166876970012831, 0.00037239999999999723, 1.3378766500000039, 1.3356014500000069, 1.0500000000231948e-06, 0.0011533259999999888, 1]
        print(f"Process {i} beginning!")
        # limits = True if i % 2 == 0 else False
        multiprocessing.Process(target=program,
                                args=(i, og_sum, *coeff_arr)).start()


def comparison_method(method, final_sum_arr, num_split=10):
    attempt_sections = np.split(final_sum_arr, num_split)
    goal_sections = np.split(goal_arr, num_split)
    summation = None
    if method == 0:
        sums = np.array(
            [sum(abs(goal_sections[i] - attempt_sections[i])) for i in
             range(num_split)])
        summation = sum(sums[2:6])
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
                                  num_split=10)
    return summation, sum_out


def pass_filter(hpf, input_arr, TC, G):
    hpf_arr = np.zeros(10000)
    lpf_arr = np.zeros(10000)
    for i in range(1, len(input_arr)):
        hpf_arr[i] = G * input_arr[i - 1] - lpf_arr[i - 1]
        lpf_arr[i] = TC * hpf_arr[i] + lpf_arr[i - 1]
    if hpf:
        return hpf_arr
    return lpf_arr


if __name__ == '__main__':
    main()
