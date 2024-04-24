from math import sqrt
import numpy as np
import pandas as pd
import draw_chart


class memwa:

    def __init__(self):
        global memwa_points, ucl, lcl
        memwa_points, ucl, lcl = [], [], []

    def gen(self, path_file):
        global memwa_points, ucl, lcl
        table_excel = pd.read_excel(f'{path_file}')  # start excel file
        data_list = []  # Data to analyze
        for i in range(len(table_excel.columns)):  # get all columns from table
            data_list.append(table_excel.values[:, i])

        data_list = np.array(data_list).transpose()  # transpose for correct work
        lamda = 0.2  # constant for memwa
        L = 1  # const of control limits
        avg_list = []  # list of average values1
        memwa_points = []

        for i in data_list:
            cur_list = []
            for cur in i:
                cur_list.append(cur)
            avg_list.append(sum(cur_list) / len(cur_list))

        sum_avg = 0

        for i in range(len(avg_list) // 2):  # get first half average value
            sum_avg += avg_list[i]
        avg = sum_avg / (len(avg_list) // 2)  # get average value

        for i in range(len(data_list)):
            if i == 0:  # TODO - Analyze the first point
                memwa_points.append(lamda * avg + (1 - lamda) * avg_list[i])
                continue
            memwa_points.append(lamda * avg_list[i] + (1 - lamda) * memwa_points[i - 1])

        T = sum(memwa_points) / len(memwa_points)  # target value
        ucl = []
        lcl = []
        sigma_list = []  # get sigma for each subgroup

        for i in range(len(data_list)):
            n = len(data_list[i])
            sigma = np.var(data_list[i]) * n / (n - 1) if n > 1 else np.var(data_list[i])
            sigma_list.append(sigma)
        sigma_avg = sum(sigma_list) / len(sigma_list)

        if sigma_avg == 0:  # if all subgroups have one value then sigma_avg = 0
            cur_subgroup = []
            for i in data_list:
                for j in i:
                    cur_subgroup.append(j)
            sigma_avg = np.var(cur_subgroup) / 2
        sigma_avg /= 2
        for i in range(len(data_list)):  # get each limit
            if i == 0:
                sigma_i = L * sigma_avg * sqrt(((lamda) / (2 - lamda)) * (1 - (1 - lamda) ** ((2 * (i + 1)))))
            else:
                sigma_i = L * sigma_avg * sqrt(((lamda) / (2 - lamda)) * (1 - (1 - lamda) ** ((2 * (i + 1)))))
            ucl.append(T + sqrt(sigma_i))
            lcl.append(T - sqrt(sigma_i))
        draw_chart.draw_chart(points=memwa_points, ucl=ucl, lcl=lcl, CL=T, name='MEWMA Chart')

    def allData(self):
        return memwa_points, ucl, lcl

    def memwaPoints(self):
        return memwa_points

    def memwaLimitUp(self):
        return ucl

    def memwaLimitDown(self):
        return lcl
