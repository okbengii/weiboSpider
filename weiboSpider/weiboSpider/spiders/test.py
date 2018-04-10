import datetime

def compare_time():
    strftime = datetime.datetime.strptime("2017-11-02", "%Y-%m-%d")
    strftime2 = datetime.datetime.strptime("2017-01-04", "%Y-%m-%d")

    now_time = datetime.date.today()
    thrDay = now_time + datetime.timedelta(days=-3)
    print now_time
    print thrDay>strftime
    print strftime>strftime2
if __name__ == "__main__":
    compare_time()