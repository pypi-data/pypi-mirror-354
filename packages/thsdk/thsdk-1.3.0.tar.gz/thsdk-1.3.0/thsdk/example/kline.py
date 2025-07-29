from thsdk import THS, Interval, Adjust
import pandas as pd
import time
from datetime import datetime
from zoneinfo import ZoneInfo

bj_tz = ZoneInfo('Asia/Shanghai')

with THS() as ths:
    # 查询历史近100条日k数据
    response = ths.klines("USHA600519", count=100)
    print("查询历史近100条日k数据:")
    print(pd.DataFrame(response.payload.result))
    time.sleep(1)

    # 查询历史20240101 - 202050101 日k数据
    response = ths.klines("USHA600519",
                          start_time=datetime(2024, 1, 1).replace(tzinfo=bj_tz),
                          end_time=datetime(2025, 1, 1).replace(tzinfo=bj_tz))
    print("查询历史20240101 - 20250101 日k数据:")
    print(pd.DataFrame(response.payload.result))
    time.sleep(1)

    # 查询历史100条日k数据 前复权
    response = ths.klines("USHA600519", count=100, adjust=Adjust.FORWARD)
    print("查询历史100条日k数据 前复权:")
    print(pd.DataFrame(response.payload.result))
    time.sleep(1)

    # 查询历史100个1分钟k数据
    response = ths.klines("USHA600519", count=100, interval=Interval.MIN_1)
    print("查询历史100个1分钟k数据:")
    print(pd.DataFrame(response.payload.result))
    time.sleep(1)
