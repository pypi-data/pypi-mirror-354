from thsdk import THS
import pandas as pd
import time


def main():
    ths = THS()
    try:
        # 连接到行情服务器
        response = ths.connect()
        if response.errInfo != "":
            print(f"登录错误:{response.errInfo}")
            return

        response = ths.block_data(0xE)
        df = pd.DataFrame(response.payload.result)
        usza_codes = df[df['代码'].str.startswith('USZA')]['代码'].tolist()
        response = ths.stock_market_data(usza_codes)
        print("股票市场数据:")
        # pd.set_option('display.max_columns', None)
        print(pd.DataFrame(response.payload.result))

        print("查询成功 数量:", len(response.payload.result))

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # 断开连接
        ths.disconnect()
        print("Disconnected from the server.")

    time.sleep(1)


if __name__ == "__main__":
    main()
