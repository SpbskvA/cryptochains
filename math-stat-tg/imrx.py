import pandas as pd
import draw_chart


class imr_x:

    def __init__(self):
        global data_list, imr_list, UCLx, LCLx, UCLmr, LCLmr
        data_list, imr_list = [], []
        UCLx, LCLx, UCLmr, LCLmr = 0, 0, 0, 0

    def gen(self, path_file):
        global data_list, imr_list, UCLx, LCLx, UCLmr, LCLmr
        table_excel = pd.read_excel(str(path_file))
        for i in range(len(table_excel.columns)):
            data_list.append(list(table_excel.values[:, i]))

        for i in range(1, len(data_list[0])):  # MR = |x(i+1) - xi|
            imr_list.append(abs(data_list[0][i - 1] - data_list[0][i]))

        CL = sum(data_list[0]) / len(data_list[0])
        imr_avg = sum(imr_list) / len(imr_list)

        # constants for i_mr control chart (size of subgroup = 1)
        E2 = 2.66
        D3 = 0
        D4 = 3.267
        UCLx = CL + E2 * imr_avg
        LCLx = CL - E2 * imr_avg
        UCLmr = D4 * imr_avg
        LCLmr = D3 * imr_avg
        draw_chart.draw_chart(points=data_list[0], ucl=[UCLx], lcl=[LCLx], CL=CL, name='I-Chart')
        draw_chart.draw_chart(points=imr_list, ucl=[UCLmr], lcl=[LCLmr], CL=imr_avg, name='MR-Chart', shift=1, start=1)

    def AllData(self):
        return data_list, imr_list

    def mrPoints(self):
        return imr_list

    def iPoints(self):
        return data_list[0]

    def iLimitUp(self):
        return UCLx

    def iLimitDown(self):
        return LCLx

    def mrLimitUp(self):
        return UCLmr

    def mrLimitDown(self):
        return LCLmr
