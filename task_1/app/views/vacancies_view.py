import json
from pprint import pprint

import ujson as ujson
from flask import Blueprint, render_template, request, session, redirect, url_for

from task_1.app import app, db_session
from task_1.app.controllers.vacancies_controller import get_vacancies_list
from task_1.app.models import Vacancies

vacancies_view = Blueprint('vacancies_view', __name__, static_folder='static', template_folder='templates')


class RequiredException(Exception):
    pass

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('vacancies'))


@app.route('/vacancies', methods=['GET', 'PUT'])
def vacancies():
    print('++' * 10)
    print(request.method)
    print('++' * 10)
    if request.method == 'PUT':
        try:
            data = {}
            for key, value in request.form.items():
                value = value[0] if isinstance(value, list) else value
                if key == 'salary':
                    # int('123.4') -> Exception
                    # float('123.4') -> 123.4 <- float('123410e-3')
                    # int(123.4) -> 123
                    value = int(float(value))
                data[key] = value

            # rm code below if empty values are allowed
            if any(not bool(v) for v in data.values()):
                raise RequiredException('All columns must contain non-empty value')

            new_vacancy = Vacancies(**data)
            print(new_vacancy)
            db_session.commit()
            return json.dumps({'success': True})
        except ValueError:
            db_session.rollback()
            return json.dumps({'error': True, 'type': 'salary'})
        except Exception as e:
            print(str(e))
            db_session.rollback()
            return json.dumps({'error': True})


    vacancies_list = get_vacancies_list()
    print(vacancies_list)
    content = {'vacancies_list': vacancies_list}
    return render_template('vacancies.html', **content)


@app.route('/vacancies/<idx>', methods=['GET', 'DELETE'])
def vacancy(idx):
    print(idx)
    return redirect(url_for('vacancies'))
