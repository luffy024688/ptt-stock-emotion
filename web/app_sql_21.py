from flask import Flask, render_template, request, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#import recognition.load_model as model # model


app = Flask(__name__)

### 設定
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 資料庫連線
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/products" #
# [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy() 
db.init_app(app)


#  create table
class Product(db.Model):
    __tablename__ = 'product'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(30), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(
        db.String(100), unique=True, nullable=False)
    description = db.Column(
        db.String(255), nullable=False)
    state = db.Column(
        db.String(10), nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)

    def __init__(self, name, price, img, description, state):
        self.name = name
        self.price = price
        self.img = img
        self.description = description
        self.state = state



# index.html
@app.route('/')  # @是裝飾器
def index():
    # return 'Hello my flask!'
    return render_template('index.html',   #渲染
                           page_header="page_header",  # 變數
                           current_time=datetime.utcnow())

## data
@app.route('/create')
def create():
    #創建table
    # db.create_all()

    # Add data   -  注意unique column
    p1 = Product('Isacc2', 8888, 'https://picsum.photos/id/1047/1200/6002', '', '')
    p2 = Product('Dennis2', 9999,'https://picsum.photos/id/1049/1200/6002', '', '')
    p3 = Product('Joey2', 7777, 'https://picsum.photos/id/1033/1200/6002', '', '')
    p = [p1, p2, p3]

    db.session.add_all(p) #db.session.add(p1)
    db.session.commit()

    return 'ok'

#--------------------
import pymysql.cursors
#使用pymysql指令來連接數據庫
cnx=pymysql.connect(host='localhost',user='root',db='products',cursorclass=pymysql.cursors.DictCursor
)
@app.route('/query', methods=['GET', 'POST'])
def query():
    cursor = cnx.cursor()
    sql = "SELECT * from product"
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
