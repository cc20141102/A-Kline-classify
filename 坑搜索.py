from kline import get_kline_json
import json
import time
import pandas as pd
import os





with open("80est.json",'r',encoding='utf8') as f:
    sz_data = json.load(f)

    
codelist=[]
daylist = []
inputlist = sz_data['codelist']



for code in inputlist:
    #print(code)
    if list(code)[0] == "0":
        code = "SZ"+code
    else:
        code = "SH"+code
    try:
        df = get_kline_json(code,120,'2023-03-24 18:00:00')
    except:
        continue
    
    cond1 = (df['low'] >= df['MA20']-0.02) & (df['low'] < df['MA10']) & (df['low'] < df['MA20']*1.01)


    # 计算条件3：该日期前至少有10个交易日数据，之后有至少5个交易日数据
    cond3 = pd.RangeIndex(len(df)).isin(range(9, len(df)-4))

    # 计算最终的条件：满足条件1、条件2和条件3
    cond = cond1 & cond3



    selected_index = df[cond == True].index
    final_idxlist = []
    for idx in selected_index:
        
        if df['close'].iloc[idx-5:idx].gt(df['MA20'].iloc[idx-5:idx]).all():
            date_str = time.strftime("%Y%m%d", time.strptime(df['timestamp'].iloc[idx], "%Y-%m-%d %H:%M:%S"))
            selected_df = df.iloc[idx-9:idx+1]
            max_close = df['close'].iloc[idx:idx+6].max()
            min_close = df['close'].iloc[idx:idx+6].min()
            next_open = df['open'].iloc[idx+1]
            print("股票代码{},日期{}，涨幅为{:.2f},最大回撤{:.2f}".format(str(code),date_str, max_close/next_open,min_close/next_open-1))
            if max_close/next_open >= 1.15 and min_close/next_open > 1.00:
                filename = os.path.join('1',str(code)+"-"+date_str+'.xlsx')
                selected_df.to_excel(filename, index=False)
            elif max_close/next_open > 1.0  and min_close/next_open > 0.98:
                filename = os.path.join('0',str(code)+"-"+date_str+'.xlsx')
                selected_df.to_excel(filename, index=False)
            elif min_close/next_open < 0.95:
                filename = os.path.join('-1',str(code)+"-"+date_str+'.xlsx')
                selected_df.to_excel(filename, index=False)
