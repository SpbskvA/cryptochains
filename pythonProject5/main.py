import time
from audioop import reverse
from operator import itemgetter

import requests
from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.chrome.options import Options

need = ["Hotbit", "Binance", "Huobi", "OKX", "Bilaxy", "Gate.io", "Kraken", "AEX", "Uniswap(v2)"]

len_need, len_other, double_chain, count_chain = 0, 0, 0, 0

# all_crypto = [['43', 'Е', 'WAXP/BTC', '$0.050602', '4.45%', '$0', '$0', '$66,145', '1.56%', '1'], ['43', 'XT.COM', 'WAXP/BTC', '$0.050602', '4.45%', '$0', '$0', '$66,145', '1.56%', '2'], ['43', 'XT.COM', 'WAXP/BTC', '$0.050602', '4.45%', '$0', '$0', '$66,145', '1.56%', '3'], ['43', 'С', 'WAXP/BTC', '$0.050602', '4.45%', '$0', '$0', '$66,145', '1.56%', '4']]
all_crypto = []


def get_info(url):
    r = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    c = urlopen(r).read()
    return BeautifulSoup(c, "html.parser")


def rework(list):
    cnt = 0
    ind = -1
    for it in list:
        if "/" in it:
            ind = cnt
            break
        cnt += 1
    cnt = 0
    for i in range(2, ind):
        list[1] += list[i]
    for i in range(ind - 2):
        list.pop(2)
    for it in list:
        try:
            if it.isdigit() or it[-1] == '%' or it[0] == '$':
                continue
        except IndexError:
            continue
        if it.upper() == it and cnt > ind:
            list.remove(it)
            ind -= 1
        elif it.lower() == it:
            list.remove(it)
            ind -= 1
        cnt += 1
    isDel = False
    for it in list:
        if it == []:
            continue
        if "/" in it:
            isDel = True
            continue
        try:
            if isDel and it == it.upper() and it[0] != '$' and it[-1] != '%':
                list.remove(it)
        except IndexError:
            pass

    for it in list:
        if "Live" in it or "Chart" in it or "ago" in it or "Updated" in it:
            list.remove(it)


def toNum(s):
    s = s.replace('$', "")
    s = s.replace('%', "")
    s = s.replace(',', '')
    try:
        float(s)
    except ValueError:
        return -1.0
    return float(s)


def value_volume(num, volume, list):
    new = []
    for x in list:
        if len(x) == 9 and toNum(x[-1]) >= volume and (num == -1 or toNum(x[-2]) >= num):
            new.append(x)
    return new


def third():
    for i in range(1, len(all_crypto) - 1, 2):
        global double_chain
        for j in range(double_chain, len(all_crypto) - 1, 2):
            if all_crypto[i][1] == all_crypto[j][1] and i - j != 1:
                pers1 = 100 * toNum(all_crypto[i][3]) / toNum(all_crypto[i - 1][3]) - 100
                pers2 = 100 * toNum(all_crypto[j + 1][3]) / toNum(all_crypto[j][3]) - 100
                f2 = open('double_chains.txt', 'a')
                f2.write(all_crypto[i - 1][0] + " " + all_crypto[i - 1][1] + " " + all_crypto[i - 1][2] + " " +
                         all_crypto[i - 1][3] + " " + all_crypto[i - 1][-2] + " " + all_crypto[i - 1][-1] + "\n")
                f2.write(
                    all_crypto[i][0] + " " + all_crypto[i][1] + " " + all_crypto[i][2] + " " + all_crypto[i][3] + " " +
                    all_crypto[i][-2] + " " + all_crypto[i][-1] + "\n")
                f2.write(str(pers1) + "%\n")
                f2.write(
                    all_crypto[j][0] + " " + all_crypto[j][1] + " " + all_crypto[j][2] + " " + all_crypto[j][3] + " " +
                    all_crypto[j][-2] + " " + all_crypto[j][-1] + "\n")
                f2.write(all_crypto[j + 1][0] + " " + all_crypto[j + 1][1] + " " + all_crypto[j + 1][2] + " " +
                         all_crypto[j + 1][3] + " " + all_crypto[j + 1][-2] + " " + all_crypto[j + 1][-1] + "\n")
                f2.write(str(pers2) + "%\n")
                f2.write("sum = " + str(pers1 + pers2) + "%\n")
                f2.write("--" * 20)
                f2.write("\n")
                double_chain = j + 2
                global count_chain
                count_chain += 1


def chain(arr, count, url):
    ln = min(len(arr), count)
    arr1 = arr[::-1]
    if arr == []:
        return
    for i in range(0, ln):
        try:
            pers = 100 * toNum(arr1[i][3]) / toNum(arr[i][3]) - 100
        except ZeroDivisionError:
            continue
        if pers > 3 and arr[i][1] in need and arr1[i][1] in need:
            f = open('need_stock_markets(10).txt', 'a')
            f.write(url + "\n")
            f.write(arr[i][0] + " " + arr[i][1] + " " + arr[i][2] + " " + arr[i][3] + " " + arr[i][-2] + " " + arr[i][
                -1] + "\n")
            f.write(
                arr1[i][0] + " " + arr1[i][1] + " " + arr1[i][2] + " " + arr1[i][3] + " " + arr1[i][-2] + " " + arr1[i][
                    -1] + "\n")
            f.write(str(pers) + "%\n")
            f.write('-' * 30 + "\n")
            global len_need
            len_need += 1
        elif pers > 3:
            f1 = open('other_stock_markets.txt', 'a')
            f1.write(url + "\n")
            f1.write(arr[i][0] + " " + arr[i][1] + " " + arr[i][2] + " " + arr[i][3] + " " + arr[i][-2] + " " + arr[i][
                -1] + "\n")
            f1.write(
                arr1[i][0] + " " + arr1[i][1] + " " + arr1[i][2] + " " + arr1[i][3] + " " + arr1[i][-2] + " " + arr1[i][
                    -1] + "\n")
            f1.write(str(pers) + "%\n")
            f1.write('-' * 30 + "\n")
            global all_crypto
            global len_other
            all_crypto.append(arr[i])
            all_crypto.append(arr1[i])
            len_other += 1


r = 20
cnt = 0
allHref = []


def check(url):
    global cnt, cnt
    print(url)
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html)
    t = soup.find_all("tr")
    l = []
    driver.execute_script("window.scrollTo(0, -1)")
    for x in t:
        list = x.text.split()
        for i in range(1, len(list) - 1):
            list[i] = list[i].replace("*", "")
        rework(list)
        if list[0].isdigit():
            list.pop()
            l.append(list)
        rework(list)
    try:
        l.sort(key=itemgetter(3, 3))
    except IndexError:
        pass
    chain(value_volume(-1, 0.1, l), 100, url)
    global cnt
    cnt += 1
    if cnt % 3 == 0:
        third()
        cnt = 0
    print('*' * 30)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "need:", len_need, "other:", len_other, "double:", count_chain)


for i in range(1, r):
    soup = get_info(f"https://www.coingecko.com/?page={r}")
    for link in soup.find_all('a'):
        s = link.get('href')
        if s == None:
            continue
        if "/en/coins/" in s and "?" not in s:
            allHref.append(s)

for item in allHref:
    check(f"https://www.coingecko.com{item}#markets")
