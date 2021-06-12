import time
import requests
from bs4 import BeautifulSoup
import re
import csv
import random
import pandas as pd


## get href
i = 1
ls_href = []
ls_href_error_p = []
st = time.time()
for i in range(1,5007): #range(1,5007)
    print(i)
    try:
        # url = 'https://www.ptt.cc/bbs/Stock/search?page='+str(i)+'&q=%E7%96%AB%E6%83%85'
        url = 'https://www.ptt.cc/bbs/Stock/index' + str(i) + '.html'
        response = requests.get(url) #目前為stock版搜尋關鍵字:疫情
        response.encoding = 'utf-8'
        sp = BeautifulSoup(response.text, 'lxml')
        #title = sp.select('.title')[0].get_text()
        #href = 'https://www.ptt.cc/' + sp.select('.title')[0].a.get('href')
        href = ['https://www.ptt.cc/' + l.a['href'] for l in sp.find_all(class_ ='title') ]
        ls_href.extend(href)
        i=i+1
        time.sleep(random.randint(0,1)) 
    except:
        print('error:',i)
        ls_href_error_p.append(i)
print(time.time()-st,'s')
pd.DataFrame(ls_href).to_csv('./data/href2.csv',index= False)
pd.DataFrame(ls_href_error_p).to_csv('./data/href_error_page2.csv',index= False)