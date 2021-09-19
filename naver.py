import enum
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///navernews.db', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)

class NewsSchema(Base):
    __tablename__ = 'navernews'

    id = Column(Integer, primary_key=True)
    date = Column(String)
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

Base.metadata.create_all(engine)
session = Session()

# def save(data):
#     session = Session()
#     new_data = NewsSchema(data["date"], data["title"]....어쩌구)
#     session.add(new_data)
#     session.commit()
#     session.close()

def parse_itnews(itnews_headline, itnews, i):
    # global result_array
    result_array=[]
    for index, news in enumerate(itnews_headline):
        result={}
        a_inx=0
        img=news.find("img")
        if img:
            a_inx=1 #img 태그가 있으면 1번째 a 태그의 정보를 사용
            
        title=news.find_all("a")[a_inx].get_text().strip()
        description=news.find("dd").find("span","lede").get_text().strip()
        link= news.find_all("a")[a_inx]["href"]
        print("{}. {}".format(index+1,title))
        print("{}".format(description))
        print("  (링크 : {})".format(link))
        #result={"{}. {}".format(index+1,title)," (링크 : {})".format(link)}

        result={"date":datetime.strptime(str(i),'%Y%m%d').strftime('%Y-%m-%d'), "title":title,"description":description,"link":link}
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
        print("{}. {}".format(index+11,title))
        print("{}".format(description))
        print("  (링크 : {})".format(link))
        #result={"{}. {}".format(index+1,title)," (링크 : {})".format(link)}

        result={"date":datetime.strptime(str(i),'%Y%m%d').strftime('%Y-%m-%d'), "title":title, "description":description, "link":link}
        result_array.append(result)
    return result_array

    

# ========= [Naver IT News] ==========
def naver_news():
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'} # 한글페이지 반환

    file=open("./news.json","w",encoding="utf-8")
    date=int(datetime.today().strftime('%Y%m%d'))
    result_array_naver = []

    for i in range(date,date-5,-1):
        pagenum = 1
        while 1:
            naver_news_url=f'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid2=732&sid1=105&date={i}&page={pagenum}'
            print('date=',i)
            print(naver_news_url)
            res = requests.get(naver_news_url, headers = headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'lxml')

            itnews_headline=soup.find('ul',attrs={'class':'type06_headline'}).find_all('li')
            itnews=soup.find('ul',attrs={'class':'type06'})
            itnews_span_tag=soup.find('span',attrs={'class':'lede'})
            if itnews != None:
                itnews = itnews.find_all('li')

            result_array_naver.extend(parse_itnews(itnews_headline, itnews, i))

           
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
            

    file.write(json.dumps(result_array_naver, ensure_ascii=False,indent=2))
    file.close()
    print()
    return result_array_naver

if __name__ == "__main__":
    result_array_if = naver_news()

    print(result_array_if)
    print("??????????????????????????")

    # db insert
    for raw_data in result_array_if:
        print(len(raw_data['link']))
        input_data = NewsSchema(
        # id=raw_data['id'],
        date=raw_data['date'],
        title=raw_data['title'],
        description=raw_data['description'],
        link=raw_data['link']
        )
        #news_item = NewsSchema("id","date", "title", "description", "link")
        session.add(input_data)
        session.commit()

    items = session.query(NewsSchema).all()
    news_dict = []
    for item in items:
    ## 읽은 DB를 dict 자료형으로 변환
    # print(item.as_dict())
        news_dict.append(item.as_dict())
    print(news_dict)

