from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Click(Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True)
    user = Column(String(15))
    comment = Column(String(75))
    style = Column(String())
    timestamp = Column(Integer())

    def __repr__(self):
        return f"Click(id={self.id}, user='{self.user}', comment='{self.comment}', style='{self.style}', timestamp={self.timestamp})"


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    user = Column(String(15))
    name = Column(String(75))
    timestamp = Column(Integer)

    def __repr__(self):
        return f"Event(id={self.id}, user='{self.user}', name='{self.name}', timestamp={self.timestamp})"


class User(Base):
    __tablename__ = "users"

    name = Column(String(15), primary_key=True)
    clicks = Column(Integer)
    events = Column(Integer)

    def __repr__(self):
        return f"Click(name='{self.name}', clicks={self.clicks}, events={self.events})"


class Hour(Base):
    __tablename__ = "hours"

    timestamp = Column(Integer, primary_key=True)
    clicks = Column(Integer)
    events = Column(Integer)

    def __repr__(self):
        # return f"Hour(timestamp='{self.timestamp}', clicks_total={self.clicks_total}, clicks={self.clicks}, events_total={self.events_total}, events={self.events})"
        return f"Hour(timestamp='{self.timestamp}', clicks={self.clicks}, events={self.events})"


class Total(Base):
    __tablename__ = "total"

    timestamp = Column(Integer, primary_key=True)
    clicks = Column(Integer)
    events = Column(Integer)

# class Stats(Base):
#     __tablename__ = "stats"

#     id = Column(Integer, primary_key=True)
#     total = Column(Integer)
#     today = Column(Integer)
#     hour = Column(Integer)

#     def __repr__(self):
#         return f"Stats(total='{self.total}', today={self.today}, hour={self.hour})"
