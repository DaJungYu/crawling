#DB추가
# ===================================================
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *

engine = create_engine('sqlite:///Securitynews.db', echo=True)
Base = declarative_base()

class NewsSchema(Base):
    __tablename__ = 'Securitynews'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    title = Column(String)
    description = Column(String(100))
    link = Column(String(100))

    def __init__(self, date, title, description, link):
        # self.id = id
        self.date = date
        self.title = title
        self.description = description
        self.link = link

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

NewsSchema.__table__.create(bind=engine, checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()


# 크롤링 함수
def security_news():
  headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Accept-Language':'ko-KR,ko'} # 한글페이지 반환
  # 헤더를 명시안하면 크롬의 영어버전(디폴트) 기준으로 반환됨.
  
  file=open("./Security_news.json","w",encoding="utf-8")
  global result_array
  result_array = []
  #date = int(datetime.today().strftime('%Y%m%d'))

  # id=0
  status = false
  for i in range(1, 6):
    security_news_url = f'https://www.wired.com/category/security/page/{i}/'
    print('page = ', i)
    print(security_news_url)
    res = requests.get(security_news_url, headers = headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')

    itnews = soup.find('ul', attrs = {'class':'archive-list-component__items'}).find_all('li')
    links = soup.find('a', sttrs  = {'class':'archive-item-component__link'})

    
    for index, news in enumerate(itnews):
      # id+=1
      news_date = news.find('div', attrs = {'archive-item-component__byline'}).find('time').get_text()
      # timestamp=time.mktime(datetime.strptime(news_date,'%B %d, %Y').timetuple())
      timestamp = datetime.strptime(news_date,'%B %d, %Y')
      title = news.find('h2', attrs = {'archive-item-component__title'}).get_text().strip()
      description=news.find('p',attrs={'archive-item-component__desc'}).get_text().strip()
      link = 'https://www.wired.com' + news.find('a', attrs = {'archive-item-component__link'})['href']
      
      print(index+1)
      print(timestamp)
      print(title)
      print(description)
      print(link)

      # link가 DB에 저장이 되어있는지 쿼리 - 결과가 1개 이상 있더라 -> 이 반복문을 탈출
      # 또는 timestamp 
      #   status = true
      # if(status) json 저장을한다


      result={"date":timestamp, "title":title, "description":description, "link":link}
      result_array.append(result)
    print()
    
  # file.write(json.dumps(result_array, ensure_ascii=False,indent=2))
  file.close()

security_news()


for raw_data in result_array:
      
  # 중복 체크

  # link 로 
  # select * from NewsSchema where link='있는지 검색할 링크' (.all())
  already_exist = session.query(NewsSchema).filter(NewsSchema.link == raw_data['link']).count()
  if already_exist != 0:
    continue

  # INSERT INTO 테이블 이름 (열1, 열2, ...) VALUE (값1, 값2 , ….)
  # INSERT INTO NewsSchema (date, title, description, link) VALUE (raw_data['date'], ....)
  input_data = NewsSchema(
    # id=raw_data['id'],
    date=raw_data['date'],
    title=raw_data['title'],
    description=raw_data['description'],
    link=raw_data['link']
  )

  session.add(input_data)
  session.commit()

# items = session.query(NewsSchema).distinct(input_data.link).order_by(NewsSchema.date.asc())
# #items = session.query(NewsSchema).all()
# news_dict = []
# for item in items:
# ## 읽은 DB를 dict 자료형으로 변환
# # print(item.as_dict())
#     news_dict.append(item.as_dict())
# print(news_dict)