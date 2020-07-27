import threading
import time

from day01.作业 import creat_data


def page(statr_page, end_page):
    creat_data(statr_page, end_page)
    time.sleep(10)


if __name__ == '__main__':
    # t1 = threading.Thread(target=page, args=(1, 100))
    t2 = threading.Thread(target=page, args=(101, 200))
    t3 = threading.Thread(target=page, args=(201, 300))
    t4 = threading.Thread(target=page, args=(301, 400))
    t5 = threading.Thread(target=page, args=(401, 500))
    t6 = threading.Thread(target=page, args=(501, 600))
    t7 = threading.Thread(target=page, args=(601, 700))
    t8 = threading.Thread(target=page, args=(701, 800))
    t9 = threading.Thread(target=page, args=(801, 900))
    t10 = threading.Thread(target=page, args=(901, 1098), daemon=True)

    # t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    print("game over")
