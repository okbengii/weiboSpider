import datetime

def compare_time():
    strftime = datetime.datetime.strptime("2017-11-02", "%Y-%m-%d")
    strftime2 = datetime.datetime.strptime("2017-01-04", "%Y-%m-%d")

    now_time = datetime.datetime.now()
    thrDay = now_time + datetime.timedelta(days=-3)
    print thrDay>now_time
    print strftime>strftime2
if __name__ == "__main__":
    compare_time()