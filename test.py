### 필수

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///news.db', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)

class NewsSchema(Base):
    __tablename__ = 'news'

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

### 필수 끝

#### DB 쓰기 news.py

session = Session()
news_item = NewsSchema("date", "title", "description", "link")
session.add(news_item)
session.commit()

#### DB 쓰기


#### DB 읽기 app.py

session = Session()
items = session.query(NewsSchema).all()

news_dict = []
for item in items:
    ## 읽은 DB를 dict 자료형으로 변환
    # print(item.as_dict())
    news_dict.append(item.as_dict())

#### DB 읽기
