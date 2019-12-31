import threading
import colorama
import random
import time
import os
colorama.init()
colors = (
    [[], "Y", colorama.Fore.YELLOW, 0],
    [[], "R", colorama.Fore.RED, 0],
    [[], "G", colorama.Fore.GREEN, 0],
    [[], "B", colorama.Fore.BLUE, 0]
)
CIRCLE_CHAR = '●'
with open("source.txt") as f:
    tree = list("".join(f.readlines()))
ctree = tree.copy()
for i in range(len(tree)):
    char = tree[i]
    for c in colors:
        if char == c[1]:
            c[0].append(i)
            tree[i] = CIRCLE_CHAR
lock = threading.Lock()


def operate_color(c):
    while 1:
        lock.acquire()
        c[3] = not c[3]
        for i in c[0]:
            ctree[i] = (c[2] if c[3] else '') + tree[i] + colorama.Style.RESET_ALL
        res = "".join(ctree).replace("T", " ")
        os.system("cls" if os.name == "nt" else "clear")
        print(res)
        lock.release()
        time.sleep(random.uniform(0.5, 1.0))


def operate_snowflakes():
    while 1:
        snowflakes = []
        lock.acquire()
        for i in range(len(ctree)):
            char = ctree[i]
            if char == "*":
                snowflakes.append(i)
        for i in snowflakes:

            try:
                start_offset = ctree[i - 1:: -1].index('\n')
            except ValueError:
                start_offset = len(ctree[i - 1:: -1])

            try:
                end_offset = ctree[i + 1::].index('\n')
            except ValueError:
                end_offset = len(ctree[i + 1::])

            ctree[i] = 'T'

            res_offset = start_offset + end_offset + 2

            if (i + res_offset) < len(ctree) and ctree[i + res_offset] == 'T':
                ctree[i + res_offset] = '*'
            else:
                ctree[start_offset] = '*'
        res = "".join(ctree).replace("T", " ")
        os.system("cls" if os.name == "nt" else "clear")
        print(res)
        lock.release()
        time.sleep(0.05)


threads = []
for c in colors:
    t = threading.Thread(target=operate_color, args=[c])
    t.start()
    threads.append(t)
t = threading.Thread(target=operate_snowflakes)
t.start()
threads.append(t)
for t in threads:
    t.join()
colorama.deinit()
