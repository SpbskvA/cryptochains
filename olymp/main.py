import time
from audioop import reverse
from operator import itemgetter

import requests
from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService  # Similar thing for firefox also!
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.chrome.options import Options

def get_url(s):
    if s.has_attr('href'):
        return s['href']
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

def chain(arr, count):
    ln = min(len(arr), count)
    arr1 = arr[::-1]
    if arr == []:
        return
    for i in range(0, ln):
        try:
            pers = 100 * toNum(arr1[i][3]) / toNum(arr[i][3]) - 100
        except ZeroDivisionError:
            continue
        if pers > 3:
            f = open('trades.txt', 'a')
            f.write(arr[i][1] + "\n")
            f.write(arr1[i][1] + "\n")
            print(arr[i][0], arr[i][1], arr[i][2], arr[i][3], arr[i][-2], arr[i][-1])
            print(arr1[i][0], arr1[i][1], arr1[i][2], arr1[i][3], arr1[i][-2], arr1[i][-1])
            print(str(pers) + "%")
            print('-' * 30)

r = 10
allHref = []
def check(url):
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
    chain(value_volume(-1, 0.1, l), 4)
    print("**" * 20)

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
