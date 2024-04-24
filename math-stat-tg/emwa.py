from math import sqrt
import numpy as np
import pandas as pd
import draw_chart


# TODO - constant like parameters
# TODO - add comments
# TODO - add return values


class emwa:

    def __init__(self):
        global y_ewma, y_limit_up, y_limit_down
        y_ewma, y_limit_up, y_limit_down = [], [], []

    def gen(self, path_file, alpha=0.2, sigma=5.85):
        global y_ewma, y_limit_up, y_limit_down
        table_excel = pd.read_excel(f'{path_file}')
        y = table_excel.values[:, 0]
        data_list = np.array(y).tolist()
        alpha = 0.2  # const for emwa
        z_av = sum(data_list) / len(data_list)

        for i in range(len(data_list)):
            if i == 0:
                y_ewma.append(alpha * data_list[i] + (1 - alpha) * z_av)
            else:
                y_ewma.append(alpha * data_list[i] + (1 - alpha) * y_ewma[i - 1])
        for i in range(len(data_list)):
            limit = sigma * sqrt(((alpha) / (2 - alpha)) * (1 - (1 - alpha) ** ((2 * (i + 1)))))
            y_limit_up.append(z_av + limit)
            y_limit_down.append(z_av - limit)
        draw_chart.draw_chart(points=y_ewma, ucl=y_limit_up, lcl=y_limit_down, CL=z_av, name='EWMA Chart')

    def ewmaPoints(self):
        return y_ewma

    def ewmaLimitUp(self):
        return y_limit_up

    def ewmaLimitDown(self):
        return y_limit_down

    def allData(self):
        return y_ewma, y_limit_up, y_limit_down
