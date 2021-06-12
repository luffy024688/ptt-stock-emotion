import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import re
import random
import csv

ls_href = list(pd.read_csv('./data/href.csv')['0'])
print(len(ls_href))

#ls = []
#ls_href_error = []
i = 0
st = time.time()

for href in ls_href[84148:]:
    print(i)
    try:
        res = requests.get(href)
        sp = BeautifulSoup(res.text, 'lxml')

        # 'title', 'link', 'date', #'comtent', 'push'
        head = sp.select('.article-meta-value')
        author = head[0].get_text()
        title = head[2].get_text()
        d = head[3].get_text()

        ls_push = sp.select('.push')
        push = '###'.join([x.text for x in ls_push])

        t = str(sp.select('#main-content')).replace('\n','')
        content= re.match(r'.*</span></div>(.*)--',t).group(1)

        i=i+1
        time.sleep(random.randint(0,1))
        with open('./data/ptt2.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([href,d,title,content,push,author])
#         ls.append((href,d,title,content,push,author))
        
    except:
        print(href)
        i=i+1
        with open('./data/href_error2.csv', 'a') as f:
            writer2 = csv.writer(f)
            writer2.writerow([href])
        
    
print(time.time()-st,'s')
# pd.DataFrame(ls).to_csv('./data/ptt.csv',index=False)
# pd.DataFrame(ls_href_error).to_csv('./data/href_error.csv',index= False)