import requests
import time
import pandas as pd
import os


def get_kline_json(code,count,t):
    highlist = []
    lowlist = []
    closelist = []
    volumelist = []
    s_t=time.strptime(t,"%Y-%m-%d %H:%M:%S")
    mkt=str(int(time.mktime(s_t))*1000)
    cookies = {
        'xq_a_token': '450e3c30f025da10d64b5dde9f1f0999b1696641',
        'xq-dj-token': '450e3c30f025da10d64b5dde9f1f0999b1696641',
        'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjQxOTMwMjE1MzcsImlzcyI6InVjIiwiZXhwIjoxNjgyNzMyMjMwLCJjdG0iOjE2ODAxNDAyMzA0OTIsImNpZCI6IldpQ2lteHBqNUgifQ.jGpbvxpCAhBk8Y6eRrYCI30iNQmn0ftruWJUHfqlU7VkfGhuoTY1fFnJHKAAxyf9ygDIoN4WJ-iaqf32rG4luP44WUcIY4AB8PLF_vBzTXWhA4vAQNv92p2FcyQKWWKSwcL45xe3aazliv10F9Ky7Ne1cIPGsLvuhDrGFOh-Cd22QDXs9IkFSjIpcGsMhf1lYCjr3apeix9LsODw42kgaUiK2NCsCzgD-z44_mTBeABs0nhGHSFj6lvz1AVo_TEfe4H4LSn_J3xlfaB5rlZ0A6WuOI0kN_ODrvlTKiBS3tUH5HFTwxAgGKDtaNSyRPvP9CrwvNrpT37Vlo0U9mWBbQ',
        'u': '4193021537',
        'xq_is_login': '1',
    }

    headers = {
        'User-Agent': 'Xueqiu iPhone 14.10',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-Hans-CN;q=1',
        # 'Cookie': 'xq_a_token=ca5cedef6ab4a7da061ea6470494c61fc3724ce0;xq-dj-token=ca5cedef6ab4a7da061ea6470494c61fc3724ce0;xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjQxOTMwMjE1MzcsImlzcyI6InVjIiwiZXhwIjoxNjc5MDcwMDU1LCJjdG0iOjE2NzY0NzgwNTU1MjgsImNpZCI6IldpQ2lteHBqNUgifQ.NqMHk1jBx0b3JXs2VxEU4hxO0lj6MCP5MfVnd-p7DtujQv6XnxrXbfCQWDuGuyHRqOMxffCPdsDQjVy8llRGlyvXhs3BBIEZHDrfNHLuhBv6joUZy4tXgGMZEutR706wjTmwVhFjhh_YQExQZLdxJCG0Ry2WPh6GqHEtnJ0RgEhSdF3bwIc7vDjZeHJd-dTBJrOj2DeIdDa6fi9FtyQnUcElZdvJ81KrmjoJPQn4jRK_nyWXWK-RjLQ0lNIYKRzoNZC3BMv4lUH9GQ0oD_nkdiv_oyn33Q_QE6JErTTMbqwKLJlgY2qeVpBZL6oqWJ-vkhAMkTU52DNsBVqvKTR1-Q;u=4193021537;xq_is_login=1',
        'Host': 'stock.xueqiu.com',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'application/json',
        'X-Device-Model-Name': 'iPhone 14 Pro',
        'X-Device-OS': 'iOS 16.0.1',
        'X-Device-ID': '3D485ED8-2AB1-4882-8FCD-3333BEAA31E3',
    }

    params = {
        'begin': mkt,
        'count':str(-count),
        'indicator': 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance,amount,zhuli,af',
        'period': 'day',
        'symbol':code ,
        'type': 'before',
        '_': str(time.time()*1000),
        'x': '',
        '_s': '',
        '_t': ''
        }

    r = requests.get(
        'https://stock.xueqiu.com/v5/stock/chart/kline.json',
        params=params,
        cookies=cookies,

        headers=headers,
        timeout=5
        )
    #print(r.text)
    data = r.json()
    columns = data['data']['column']
    items = data['data']['item']

# 将数据转换为DataFrame
    
    selected_columns = ["timestamp", "volume", "open", "high", "low", "close", "chg", "percent", "turnoverrate", "amount", "active_buy_volume", "active_sell_volume", "un_active_buy_Volume", "un_active_sell_volume"]
    df = pd.DataFrame(items, columns=data['data']['column'])[selected_columns]
    df['timestamp'] = df['timestamp'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x/1000)))
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA30'] = df['close'].rolling(window=30).mean()
    df = df.dropna()
# 将数据写入Excel文件
    #df.to_excel('data_selected_with_MA.xlsx', index=False)
    df = df.reset_index(drop=True)
    return df


#t = '2023-3-22 18:00:00'
#df = get_kline_json('SZ000948',90,t)
#code = 'SZ000948'
#print(df)
#print(df.index)
# 计算条件1：low列的值要大于等于MA20列的值，且low列要小于MA10以及MA20乘1.01
'''cond1 = (df['low'] >= df['MA20']-0.02) & (df['low'] < df['MA10']) & (df['low'] < df['MA20']*1.01)


# 计算条件3：该日期前至少有10个交易日数据，之后有至少5个交易日数据
cond3 = pd.RangeIndex(len(df)).isin(range(9, len(df)-4))

# 计算最终的条件：满足条件1、条件2和条件3
cond = cond1 & cond3



selected_index = df[cond == True].index
final_idxlist = []
for idx in selected_index:
    
    if df['close'].iloc[idx-5:idx].gt(df['MA20'].iloc[idx-5:idx]).all():
        date_str = time.strftime("%Y%m%d", time.strptime(df['timestamp'].iloc[idx], "%Y-%m-%d %H:%M:%S"))
        selected_df = df.iloc[idx-10:idx]
        max_close = df['close'].iloc[idx:idx+5].max()
        next_open = df['open'].iloc[idx+1]
        print("日期{}，涨幅为{:.2f}".format(date_str, max_close/next_open))
        if max_close/next_open >= 1.09:
            filename = os.path.join('1',str(code)+"-"+date_str+'.xlsx')
            selected_df.to_excel(filename, index=False)
        elif max_close/next_open > 1.0  and max_close/next_open < 1.09:
            filename = os.path.join('0',str(code)+"-"+date_str+'.xlsx')
            selected_df.to_excel(filename, index=False)
        else:
            filename = os.path.join('-1',str(code)+"-"+date_str+'.xlsx')
            selected_df.to_excel(filename, index=False)'''



