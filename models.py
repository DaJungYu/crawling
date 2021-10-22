from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SecurityNews(db.Model):
    __tablename__ = 'Securitynews'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String(100))
    link = db.Column(db.String(100))

    def __init__(self, date, title, description, link):
        # self.id = id
        self.date = date
        self.title = title
        self.description = description
        self.link = link

    # def as_dict(self):
    #    return {c.name: getattr(self, c.name) for c in self.__table__.Columns}

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'date': self.date,
           'title': self.title,
           'description': self.description,
           'link': self.link
       }


class NaverNews(db.Model):
    __tablename__ = 'navernews'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String)
    link = db.Column(db.String)

    def __init__(self,  date, title, description, link):
        self.date = date
        self.title = title
        self.description = description
        self.link = link

    def as_dict(self):
        print(self.__table__)
        print("---------------")
        return {c.name: getattr(self, c.name) for c in self.__table__.Columns}

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'date': self.date,
           'title': self.title,
           'description': self.description,
           'link': self.link
       }

