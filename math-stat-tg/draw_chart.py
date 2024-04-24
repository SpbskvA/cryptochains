import matplotlib.pyplot as plt

cnt = 0  # how many charts are processing now


def check_limits(points, ucl_limit, lcl_limit, shift=0):

    line_board = len(ucl_limit) == 1 or len(lcl_limit) == 1
    ind = 0 if line_board else 1e8

    for i in range(len(points)):
        if points[i] >= ucl_limit[min(ind, i)] or points[i] <= lcl_limit[min(ind, i)]:
            plt.scatter(i + 1 + shift, points[i], s=300, c='red', marker='X')
        else:
            plt.scatter(i + 1 + shift, points[i], s=120, c='blue', marker='o')


def draw_chart(points=[], ucl=[], lcl=[], CL=None, name='', shift=0, start=0, count=1):  # size - how many charts to show | start - add to x axis | shift - shift x axis
    global cnt
    cnt += 1
    if cnt == 1:
        plt.figure(figsize=(15, 7))

    x = list(range(1, len(points) + 1 + start))  # x-axis
    x = x[shift:]  # shift x-axis if needed
    plt.plot(x, points, color='blue', label=name)

    if len(ucl) == 1:
        plt.axhline(y=ucl[0], color='green', label='UCL', linestyle='--')
    else:
        plt.plot(x, ucl, color='green', label='UCL', linestyle='--')

    if len(lcl) == 1:
        plt.axhline(y=lcl[0], color='green', label='LCL', linestyle='--')
    else:
        plt.plot(x, lcl, color='green', label='LCL', linestyle='--')

    check_limits(points, ucl, lcl, shift=shift)

    if CL is not None:
        plt.axhline(y=CL, color='red', linestyle='-', label='AVG')
    plt.xlabel('Axe x', fontsize=16)
    plt.ylabel('Axe y', fontsize=16)
    plt.xlim([0.8, len(points) + 0.2])
    plt.title(name, fontsize=30)
    plt.savefig('out//foo.png')
    if cnt == count:  # for multiple charts
        plt.show()
        cnt = 0
