from flask import Flask, render_template, request, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import numpy as np

import model.load_model as model # model


app = Flask(__name__)

### 設定
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 資料庫連線
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/ptt_stock" #
# [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy() 
db.init_app(app)


#  create table :df[['date','恐慌指數-VIX','BI','close','pos篇數','neg篇數','seg']]
class Ptt(db.Model):
    __tablename__ = 'ptt'
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime,nullable=False,unique=True) # date不適合當主key，因為資料庫處理date資料尚要轉換
     
    vix = db.Column(db.Float, nullable=True)
    BI = db.Column(db.Float, nullable=True)
    close = db.Column(db.Float, nullable=True)
    pos = db.Column(db.Float, nullable=True)
    neg = db.Column(db.Float, nullable=True)
    seg = db.Column(db.String(255), nullable=True)
    
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)

    def __init__(self, date,vix,BI,close,pos,neg,seg):
        self.date = date
        self.vix = vix
        self.BI = BI
        self.close = close
        self.pos = pos
        self.neg = neg
        self.seg = seg



#  create table: df['date','art','推文數','article連結']
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime)
    link = db.Column(db.String(255), nullable=False,unique=True)
    art =  db.Column(db.String(100),  nullable=False)
    push = db.Column(db.Integer)
    
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)

    def __init__(self, date,link,art,push):
        self.date = date
        self.link = link
        self.art = art
        self.push = push

###-----------------------------#
# index.html
@app.route('/')  # @是裝飾器
def index():
    # return 'Hello my flask!'
    return render_template('index.html',   #渲染
                           page_header="page_header",  # 變數
                           current_time=datetime.utcnow())


@app.route('/article')  # @是裝飾器
def article():
    # return 'Hello my flask!'
    return render_template('get_data.html',   #渲染
                           page_header="page_header",  # 變數
                           current_time=datetime.utcnow())

@app.route('/ptt')  # @是裝飾器
def ptt():
    d = request.args.get("bd")
    # 預設
    if d is None:
        d = '2021-05-31'
    return render_template('get_data2.html',   #渲染
                           d = d,  # 變數：html  = function內的
                           page_header="page_header",  # 變數
                           current_time=datetime.utcnow())
    # return render_template('get_data2.html',   #渲染
    #                        page_header="page_header",  # 變數
    #                        current_time=datetime.utcnow())                    
                           
# @app.route('/all')  # @是裝飾器
# def all():
#     d = request.args.get("bd")
#     # 預設
#     if d is None:
#         d = '2020-10-07'
#     # return 'Hello my flask!'
#     return render_template('get_data3_merge.html',   #渲染
#                            d = d,  # 變數：html  = function內的
#                            page_header="page_header",  # 變數
#                            current_time=datetime.utcnow())                        
                           

#---------------------------------------------------------
# ## create table
# @app.route('/create')   # flask 要在def裡面才會去運行
# def create():
#     db.create_all()
#     return 'ok'  # 沒有return會有type error

## insert data
# (date,vix,BI,close,pos,neg,seg)
@app.route('/insert_ptt')
def insert_ptt():
    df = pd.read_csv('/Users/yichinghau/Desktop/AI-course/ptt-stock-emotion/web/data/ptt.csv')
    for row in df.itertuples(index=True, name='Pandas'):
    
        p = Ptt(getattr(row, "date"), getattr(row, "vix"), getattr(row, "BI"), getattr(row, "close"),
        getattr(row, "pos"), getattr(row, "neg"), getattr(row, "seg"))
        # print(p)
        db.session.add(p ) #db.session.add(p1)
        db.session.commit() # 送出更改
    return('fininshed')

# ( date,link,art,push)
@app.route('/insert_article')
def insert_article():
    df2 = pd.read_csv('/Users/yichinghau/Desktop/AI-course/ptt-stock-emotion/web/data/article.csv')
    # for (colname,colval) in df2.iterrows():
        # a = Article(colval['date'],colval['link'],colval['art'],colval['push'])
        # print('-------------',row)    
    for row in df2.itertuples(index=True, name='Pandas'):
        a = Article(getattr(row, "date"), getattr(row, "link"), getattr(row, "art"),getattr(row, "push"))         
        db.session.add(a) 
        db.session.commit()

    return 'ok'

#--------------------
import pymysql.cursors
#使用pymysql指令來連接數據庫

@app.route('/query_article', methods=['GET', 'POST'])
def query_article():
    cnx=pymysql.connect(host='localhost',user='root',db='ptt_stock',cursorclass=pymysql.cursors.DictCursor)
    cursor = cnx.cursor()
    sql = "SELECT * from article WHERE date='2019-12-02' ORDER BY push DESC LIMIT 5"
    cursor.execute(sql)
    res=cursor.fetchall() #取出結果 fetchone() fetchall()
    cnx.close()
    return jsonify(res)
    
@app.route('/query_ptt', methods=['GET', 'POST'])
def query_ptt():
    cnx=pymysql.connect(host='localhost',user='root',db='ptt_stock',cursorclass=pymysql.cursors.DictCursor)
    d = request.args.get("bd")
    cursor = cnx.cursor()
    sql = "SELECT * from ptt WHERE date= '{}' ".format(d)   #ORDER BY push DESC LIMIT 5"
    cursor.execute(sql)
    res=cursor.fetchall() #取出結果 fetchone() fetchall()
    cnx.close()
    return jsonify(res) 

@app.route('/query_ptt_all', methods=['GET', 'POST'])
def query_ptt_all():
    cnx=pymysql.connect(host='localhost',user='root',db='ptt_stock',cursorclass=pymysql.cursors.DictCursor)
    cursor = cnx.cursor()
    sql = "SELECT * from ptt"   #ORDER BY push DESC LIMIT 5"
    cursor.execute(sql)
    res=cursor.fetchall() #取出結果 fetchone() fetchall()
    cnx.close()
    return jsonify(res)    


#---------------------------
# model
@app.route('/model', methods=['GET', 'POST'])
def get_file():
    if request.method == "GET":
        bi = request.args.get("bi")        
        bis = request.args.get("bis")
        bim = request.args.get("bim")
        try:
            data  = np.array([[float(bi),float(bis),float(bim)]])
            print('00000',data[0])
        except:
            data = np.array([[0,0,0]])
        
        
        # predict = model.recog_digit(data)[0][0]
        predict = model.predict_model(data)[0][0]
             
        return render_template('model.html', page_header="upload hand write picture",predict = predict) #

@app.route('/model2', methods=['GET', 'POST'])
def get_file2():
    if request.method == "GET":
        bi = request.args.get("bi")        
        
        try:
            data  = np.array([[float(bi)]])
            # print('00000',data)
        except:
            data = np.array([[0]])
            # print('00001',data)
        
        
        predict = model.predict_model2(data)[0]
        # print('predict:',predict)
        if predict == 1:
            p = '/static/img/up.png'
        else:
            p = '/static/img/down.png'
             
        return render_template('model2.html', page_header="upload hand write picture",p = p) #
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')