import json
from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
from Securitynews import NewsSchema
# from Securitynews import *

from models import NaverNews, SecurityNews
from naver import NewsSchema2

app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

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


@app.route('/naver_news',methods=['GET'])
def naver_news():

    result2 = []
    news2 = NaverNews.query.order_by(NewsSchema2.date.desc())

    for item in news2:
        result2.append(item.serialize)

    return jsonify(result2)




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