import requests
from bs4 import BeautifulSoup
import pandas as pd
from soupsieve import select_one

# variables
URL = 'https://www.tdcc.com.tw/smWeb/QryStockAjax.do'
STOCK_NO = 2330
DATE = '20210429'

#request
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
cookies = {'Cookie':'_ga=GA1.3.1280641936.1620822076; _gid=GA1.3.297877003.1620822076; JSESSIONID=0000Gvkk30L2svyXtBdb1ez1Xad:19tmdfnom'}
data = {'scaDates':f'{DATE}', 'scaDate':f'{DATE}', 'SqlMethod':'StockNo' ,'StockNo':f'{STOCK_NO}', 'radioStockNo':f'{STOCK_NO}', 'REQ_OPR':'SELECT',
        'clkStockNo':f'{STOCK_NO}'}
r = requests.post(URL, data=data, headers=headers, cookies=cookies)

# BeautifulSoup
soup = BeautifulSoup(r.text, 'lxml')
stock_name = soup.select('table')[6].select_one('td').text
stock_name = stock_name[stock_name.find('證券名稱：')+5:]
table = soup.select('table')[7]

# Dataframe
df = pd.read_html(table.prettify())[0]
df.columns = df.loc[0].to_list()
df = df[1:].reset_index(drop=True)
df = df.assign(stock_id=STOCK_NO, stock_name=stock_name, date=DATE)