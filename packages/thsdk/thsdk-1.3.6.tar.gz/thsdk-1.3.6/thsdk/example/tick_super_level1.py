from thsdk import THS, Interval, Adjust
import pandas as pd
import time
from datetime import datetime
from zoneinfo import ZoneInfo

with THS() as ths:
    response = ths.tick_super_level1("USZA300033")
    print("历史当日分钟数据:")
    if response.errInfo != "":
        print(f"错误信息: {response.errInfo}")
    # pd.set_option('display.max_columns', None)

    print(pd.DataFrame(response.payload.result))
    time.sleep(1)
