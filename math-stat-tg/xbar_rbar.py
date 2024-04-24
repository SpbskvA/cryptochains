import numpy as np
import pandas as pd
import draw_chart


class xbar_r:

    def __init__(self):
        global data_list, x_avg, r_avg, UCLx, LCLx, UCLr, LCLr
        data_list, x_avg, r_avg = [], [], []
        UCLx, LCLx, UCLr, LCLr = 0, 0, 0, 0

    def gen(self, path_file):
        global data_list, x_avg, r_avg, UCLx, LCLx, UCLr, LCLr
        table_excel = pd.read_excel(f'{path_file}')
        for i in range(len(table_excel.columns)):
            data_list.append(table_excel.values[:, i])

        data_list = np.array(data_list).transpose()  # get data

        n = len(data_list[0])
        for i in data_list:
            cur_list = []
            for cur in i:
                cur_list.append(cur)
            x_avg.append(sum(cur_list) / len(cur_list))
            r_avg.append(max(cur_list) - min(cur_list))

        CL = sum(x_avg) / len(x_avg)
        R = sum(r_avg) / len(r_avg)

        # constants for xbar_r control chart (size of subgroup from 2 to 8)
        A2 = [1.88, 1.02, 0.73, 0.58, 0.48, 0.42, 0.37, 0.34]
        D3 = [0, 0, 0, 0, 0.03, 0.07, 0.14, 0.18]
        D4 = [3.27, 2.57, 2.28, 2.11, 2, 1.92, 1.86, 1.82]
        UCLx = CL + A2[n - 2] * R
        LCLx = CL - A2[n - 2] * R
        UCLr = D4[n - 2] * R
        LCLr = D3[n - 2] * R

        draw_chart.draw_chart(points=x_avg, ucl=[UCLx], lcl=[LCLx], CL=CL, name='X-bar Chart')
        draw_chart.draw_chart(points=r_avg, ucl=[UCLr], lcl=[LCLr], CL=R, name='R Chart', shift=1, start=1)

    def xPoints(self):
        return x_avg

    def rPoints(self):
        return r_avg

    def allData(self):
        return data_list, x_avg, r_avg, UCLx, LCLx, UCLr, LCLr

    def xLimitUp(self):
        return UCLx

    def xLimitDown(self):
        return LCLx

    def rLimitUp(self):
        return UCLr

    def rLimitDown(self):
        return LCLr
