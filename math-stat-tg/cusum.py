import pandas as pd
import draw_chart


class cusum:

    def __init__(self):
        global data_list, imr_list, uc_list, lc_list, UCL, LCL
        data_list, imr_list, uc_list, lc_list = [], [], [], []  # MR = |x(i+1) - xi|
        UCL, LCL = 0, 0

    def gen(self, path_file):
        global data_list, imr_list, uc_list, lc_list, UCL, LCL
        table_excel = pd.read_excel(f'{path_file}')

        for i in range(len(table_excel.columns)):
            data_list.append(table_excel.values[:, i])
        for i in range(1, len(data_list[0])):
            imr_list.append(abs(data_list[0][i - 1] - data_list[0][i]))

        CL = sum(data_list[0]) / len(data_list[0])
        imr_avg = sum(imr_list) / len(imr_list)
        d3 = 1.128  # const for i-mr chart
        sigma = imr_avg / d3

        w = 1  # TODO - Choose the critical level parameter
        u = CL  # TODO - Choose the target value
        UCL = 4 * sigma  # control limit for i-mr
        LCL = -4 * sigma

        for i in range(0, len(data_list[0])):
            if i == 0:
                uc_list.append(max(0, 0 + data_list[0][i] - w - u))
                lc_list.append(min(0, 0 + data_list[0][i] + w - u))
                continue
            uc_list.append(max(0, uc_list[i - 1] + data_list[0][i] - w - u))
            lc_list.append(min(0, lc_list[i - 1] + data_list[0][i] + w - u))
        draw_chart.draw_chart(points=uc_list, ucl=[UCL], lcl=[LCL], CL=0, name='CUSUM Chart', count=2)
        draw_chart.draw_chart(points=lc_list, ucl=[UCL], lcl=[LCL], CL=0, name='CUSUM Chart', count=2)

    def allData(self):
        return uc_list, lc_list, UCL, LCL

    def cusumUpPoints(self):
        return uc_list

    def cusumDownPoints(self):
        return lc_list

    def cusumUCL(self):
        return UCL

    def cusumLCL(self):
        return LCL
