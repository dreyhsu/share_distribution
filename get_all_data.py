import pandas as pd

#requests
URL = 'https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5'
df = pd.read_csv(URL)

# manipulation
df = df[(df['持股分級'] >= 6) & (df['持股分級'] < 17)]
temp_list = df['證券代號'].unique()
def stock_id_check(item):
    if len(item) == 4:
        if '00' not in item:
            try:
                int(item)
                return item
            except ValueError:
                pass
map_object = map(stock_id_check, temp_list)
stock_id_list = list(map_object)

df = df[(df['持股分級'] >= 6) & (df['持股分級'] < 17)]
df = df[df['證券代號'].isin(stock_id_list)].groupby('證券代號').agg({'占集保庫存數比例%': 'sum'})
