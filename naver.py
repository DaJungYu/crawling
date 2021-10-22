import enum
import json
import requests
import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
from sqlalchemy.sql.sqltypes import DateTime

engine = create_engine('sqlite:///Securitynews.db', echo=True)
Base = declarative_base()

#DB
class NewsSchema2(Base):
    __tablename__ = 'navernews'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    title = Column(String)
    description = Column(String)
    link = Column(String)

    def __init__(self,  date, title, description, link):
        self.date = date
        self.title = title
        self.description = description
        self.link = link

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

NewsSchema2.__table__.create(bind=engine, checkfirst=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# def save(data):
#     session = Session()
#     new_data = NewsSchema(data["date"], data["title"]....어쩌구)
#     session.add(new_data)
#     session.commit()
#     session.close()


def parse_itnews(itnews_headline, itnews, date_today):
    #itnews_headline : top10
    #itnews : top11~20
    result_array=[] # 5. 요청 받은 것(파싱) 결과를 넣어서 리턴
    for index, news in enumerate(itnews_headline):
        result={}
        a_inx=0
        img=news.find("img")
        if img:
            a_inx=1 #img 태그가 있으면 1번째 a 태그의 정보를 사용
            
        title=news.find_all("a")[a_inx].get_text().strip()
        description=news.find("dd").find("span","lede").get_text().strip()
        link= news.find_all("a")[a_inx]["href"]
        # timestamp=datetime.strptime(str(i),'%Y%m%d').strftime('%Y-%m-%d')
        # timestamp = datetime.strptime(str(i),'%Y%m%d')
        print("{}. {}".format(index+1,title))
        print("{}".format(description))
        print("  (링크 : {})".format(link))
        #result={"{}. {}".format(index+1,title)," (링크 : {})".format(link)}

        #result={"date":datetime.strptime(str(i),'%Y%m%d').strftime('%Y-%m-%d'), "title":title,"description":description,"link":link}
        timestamp = datetime.datetime.strptime(date_today,'%Y%m%d')

        result={"date":timestamp, "title":title,"description":description,"link":link}
        result_array.append(result)

    if itnews == None:
        return result_array

    for index, news in enumerate(itnews):
        result={}
        a_inx=0
        img=news.find("img")
        if img:
            a_inx=1 #img 태그가 있으면 1번째 a 태그의 정보를 사용
            
        title=news.find_all("a")[a_inx].get_text().strip()
        description=news.find("dd").find("span","lede").get_text().strip()
        link= news.find_all("a")[a_inx]["href"]
        # timestamp=datetime.strptime(str(i),'%Y-%m-%d').strftime('%Y-%m-%d')
        # timestamp = datetime.strptime(str(i),'%Y%m%d')
        print("{}. {}".format(index+11,title))
        print("{}".format(description))
        print("  (링크 : {})".format(link))
        #result={"{}. {}".format(index+1,title)," (링크 : {})".format(link)}

        timestamp = datetime.datetime.strptime(date_today,'%Y%m%d')

        result={"date":timestamp, "title":title, "description":description, "link":link}
        result_array.append(result)
    return result_array

    

# ========= [Naver IT News] ==========
def naver_news():
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'} # 한글페이지 반환

    file=open("./news.json","w",encoding="utf-8")
    date_today = datetime.datetime.now()
    print(date_today)

    result_array_naver = [] # 3. 빈 리스트에 크롤링 파싱 결과를 축적.

    for i in range(5):
        date_format = date_today.strftime("%Y%m%d")
        pagenum = 1
        while 1:
            naver_news_url=f'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid2=732&sid1=105&date={date_format}&page={pagenum}'
            print('date=',date_format)
            print(naver_news_url)
            res = requests.get(naver_news_url, headers = headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'lxml')

            itnews_headline=soup.find('ul',attrs={'class':'type06_headline'}).find_all('li')
            itnews=soup.find('ul',attrs={'class':'type06'})
            itnews_span_tag=soup.find('span',attrs={'class':'lede'})
            if itnews != None:
                itnews = itnews.find_all('li')

            result_array_naver.extend(parse_itnews(itnews_headline, itnews, date_format)) # 4. parse_itnews에서 파싱한 데이터 리스트를 받아서 for문(페이지 별)을 돌려 합침.

           
            itnews_a_tag=soup.find('div',attrs={'class':'paging'}).find_all("a") # findall로 a태그를 전부 가져온다
            if itnews_a_tag == None: # 페이지 없을때 None 나오는지 체크
                break

            status = False

            for page in itnews_a_tag:
                number=int(page.get_text())
                # print(pages)
                if number > pagenum:
                    status = True
                    pagenum=pagenum+1
                    break

            if status:
                continue
            else:
                break
            
            # itnews_a_tag를 for문 돌려서 모든 a태그의 내용(페이지 숫자)을 보면서
            # pagenum 보다 큰 게 있으면 -> pagenum 업데이트 하고 continue

            # paging의 a태그의 text를 뽑아서 이 다음 페이지의 링크가 있는지 본다
            # 링크가 없으면 break해서 while 1 탈출
            
        # date -= datetime.timedelta(days=1).strftime("%Y%m%d")
        date_today -= timedelta(days=1)  
    #print("result_array_naver:",result_array_naver)    
    #file.write(json.dumps(result_array_naver, ensure_ascii=False,indent=2))
    file.close()
    print()
    return result_array_naver

if __name__ == "__main__":
    result_array_if = naver_news() #1. 새로운 news data를 갖고 옴.(정제시킨 데이터)

    
    print(result_array_if)
    print("??????????????????????????")

    # db insert
    for raw_data in result_array_if:
        # 2. 중복 체크
        # select * from NewsSchema where link='있는지 검색할 링크' (.all())
        already_exist = session.query(NewsSchema2).filter(NewsSchema2.link == raw_data['link']).count()
        if already_exist != 0:
            continue

        #print(len(raw_data['link']))
        input_data = NewsSchema2(
        # id=raw_data['id'],
        date=raw_data['date'],
        title=raw_data['title'],
        description=raw_data['description'],
        link=raw_data['link']
        )
        #news_item = NewsSchema("id","date", "title", "description", "link")
        session.add(input_data)
        session.commit()

    # items = session.query(NewsSchema).all()
    # news_dict = []
    # for item in items:
    # ## 읽은 DB를 dict 자료형으로 변환
    # # print(item.as_dict())
    #     news_dict.append(item.as_dict())
    # print(news_dict)