import datetime
import pytz


# Return the datetime in HK timezone
def hk_time_now():
    hong_kong_tz = pytz.timezone("Asia/Hong_Kong")
    return datetime.datetime.now(tz=hong_kong_tz)
