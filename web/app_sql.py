from flask import Flask, render_template, request, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd

#import recognition.load_model as model # model


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
cnx=pymysql.connect(host='localhost',user='root',db='ptt_stock',cursorclass=pymysql.cursors.DictCursor
)
@app.route('/query', methods=['GET', 'POST'])
def query():
    cursor = cnx.cursor()
    sql = "SELECT * from article"
    cursor.execute(sql)
    res=cursor.fetchall() #取出結果 fetchone() fetchall()

    return jsonify(res)






## model
# @app.route('/model', methods=['GET', 'POST'])
# def get_file():
#     if request.method == "GET":
#         return render_template('file.html', page_header="upload hand write picture")
#     elif request.method == "POST":
#         file = request.files['file']
#         if file:
#             filename = str(uuid.uuid4())+"_"+file.filename
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
#             predict = model.recog_digit(filename)
#         return render_template('recog_result.html', page_header="hand writing digit recognition", predict = predict, src = url_for('static', filename=f'uploaded/{filename}'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
