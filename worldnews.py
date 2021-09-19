import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///Securitynews.db', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)

class NewsSchema(Base):
    __tablename__ = 'Securitynews'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    title = Column(String)
    description = Column(String)
    link = Column(String)

    def __init__(self, date, title, description, link):
        self.date = date
        self.title = title
        self.description = description
        self.link = link

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

Base.metadata.create_all(engine)


def security_news():
  headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Accept-Language':'ko-KR,ko'} # 한글페이지 반환
  # 헤더를 명시안하면 크롬의 영어버전(디폴트) 기준으로 반환됨.
  
  file=open("./Security_news.json","w",encoding="utf-8")
  result_array = []
  date = int(datetime.today().strftime('%Y%m%d'))

  for i in range(1, 4):
    security_news_url = f'https://www.wired.com/category/security/page/{i}/'
    print('page = ', i)
    print(security_news_url)
    res = requests.get(security_news_url, headers = headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')

    itnews = soup.find('ul', attrs = {'class':'archive-list-component__items'}).find_all('li')
    links = soup.find('a', sttrs  = {'class':'archive-item-component__link'})

    for index, news in enumerate(itnews):
      news_date = news.find('div', attrs = {'archive-item-component__byline'}).find('time').get_text()
      title = news.find('h2', attrs = {'archive-item-component__title'}).get_text().strip()
      description=news.find('p',attrs={'archive-item-component__desc'}).get_text().strip()
      link = 'https://www.wired.com' + news.find('a', attrs = {'archive-item-component__link'})['href']
      print(index+1)
      print(news_date)
      print(title)
      print(description)
      print(link)
      result={"id": index+1, "date":news_date, "title":title, "description":description, "link":link}
      result_array.append(result)
    print()

  session = Session()

  for raw_data in result:
    print(raw_data)
    input_data = NewsSchema(
      id=raw_data['id'],
      date=raw_data['date'],
      Title=raw_data['title'],
      description=raw_data['description'],
      link=raw_data['link']
  )

  #news_item = NewsSchema("id","date", "title", "description", "link")
  session.add(input_data)
  session.commit()

  session = Session()
  items = session.query(NewsSchema).all()

  news_dict = []
  for item in items:
  ## 읽은 DB를 dict 자료형으로 변환
  # print(item.as_dict())
    news_dict.append(item.as_dict())
  print(news_dict)

  file.write(json.dumps(result_array, ensure_ascii=False,indent=2))
  file.close()

security_news()