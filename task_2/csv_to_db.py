import csv
import os
import sys

from sqlalchemy import create_engine, Column, VARCHAR, Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from task_2.config import Config

EXIT_CODES = {
    200: "Добавление в базу выплнено успешно",
    404: 'Укажите путь к *.csv файлу после названия скрипта: "<scriptmane> path/to/file.csv"',
    404_1: 'Указанный файл не существует',
}

CONNECT_STRING = Config.connect_string or 'postgresql://postgres:root@localhost/test_2'
engine = create_engine(CONNECT_STRING, convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class Person(Base):
    __tablename__ = "persons"
    fio = Column(VARCHAR(255), primary_key=True)
    city = Column(VARCHAR(255))
    age = Column(Integer)
    position = Column(VARCHAR(255))

    def __init__(self, **kwargs):
        self_dir = dir(self)
        for key, value in kwargs.items():
            if key in self_dir:
                setattr(self, key, value)


def run():
    args = sys.argv

    if not len(args) > 0:
        return 404

    file_path = ''
    try:
        file_path = args[1]
    except IndexError:
        return 404

    if not os.path.exists(file_path):
        return 404_1

    errors = {}  # {str_idx: error}
    with open(file_path) as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=['fio', 'city', 'age', 'position'])
        for idx, row in enumerate(reader):
            try:
                row['age'] = int(row.get('age'))
            except ValueError:
                errors[idx] = 'Для поля age ожидалось число. Получено "%s"' % row.get('age')
                continue

            new_person = Person(**row)
            session.add(new_person)
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                if 'duplicate' in str(e):
                    errors[idx] = 'В базе данных уже есть поле с ФИО "%s"' % row.get('fio')
                else:
                    errors[idx] = str(e)
            except Exception as e:
                session.rollback()
                errors[idx] = str(e)

    return 200, errors


if __name__ == '__main__':
    result_code, errors = run()

    print(EXIT_CODES.get(result_code, 'Скрипт завершился с неизвестным статусом'))

    if len(errors):
        print('При импорте возникли некоторые ошбки:')
        for key, value in errors.items():
            print('Строка %s: %s' % (key, value))

    if session:
        session.close()
