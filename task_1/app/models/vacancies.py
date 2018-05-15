from sqlalchemy import Column, Integer, String

from task_1.app import Base, db_session

__all__ = ['Vacancies']


class Vacancies(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    salary = Column(Integer)
    experience = Column(String(255))
    city = Column(String(255))

    def __init__(self, **kwargs):
        self_dir = dir(self)
        for key, value in kwargs.items():
            if key in self_dir:
                setattr(self, key, value)
        db_session.add(self)

    def __str__(self):
        return '%s - %s' % (self.name, self.city)
