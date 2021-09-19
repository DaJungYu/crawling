import json
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
# from Securitynews import *

from models import NaverNews, SecurityNews

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Securitynews.db'

db = SQLAlchemy(app)

@app.route('/security_news',methods=['GET'])
def security_news():
    # 파일 IO로 json 읽기
    # -> DB에서 가져오기
    # with open('./Security_news.json','rt', encoding='UTF8') as f:
    #     news = json.loads(f.read())

    # return jsonify(news)


    # DB로 가져오기
    result = []
    news = SecurityNews.query.all()
    for item in news:
        result.append(item.serialize)
    return jsonify(result)




@app.route('/')
@app.route('/home')
def home():
    return 'Hello, World!'

@app.route('/user')
def user():
    return 'Hello, user!'



# if __name__=='__main__':
app.run(debug=True)

    # session = Session()
    # items = session.query(SecurityNews).all()

# news_dict = []
# for item in items:
#     ## 읽은 DB를 dict 자료형으로 변환
#     # print(item.as_dict())
#     news_dict.append(item.as_dict())
# print(news_dict)