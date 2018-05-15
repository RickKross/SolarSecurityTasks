import json

from flask import Blueprint, render_template, request, redirect, url_for

from task_1.app import app, db_session
from task_1.app.controllers.vacancies_controller import get_vacancies_list, get_vacancy, delete_vacancy
from task_1.app.models import Vacancies

vacancies_view = Blueprint('vacancies_view', __name__, static_folder='static', template_folder='templates')


class RequiredException(Exception):
    pass


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('vacancies_page'))


@app.route('/vacancies', methods=['GET', 'PUT'])
def vacancies_page():
    if request.method.lower() == 'put':
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
        except ValueError:
            db_session.rollback()
            return json.dumps({'error': 'salary'})
        except Exception as e:
            print(str(e))
            db_session.rollback()
            return json.dumps({'error': True})
        else:
            db_session.commit()
            return json.dumps({'success': True})

    vacancies_list = get_vacancies_list()
    content = {'vacancies_list': vacancies_list}
    return render_template('vacancies.html', **content)


@app.route('/vacancies/<idx>', methods=['GET', 'DELETE'])
def vacancy_page(idx):
    if request.method.lower() == 'delete':
        request_idx = request.form.get('id')
        request_idx = request_idx[0] if isinstance(request, list) and len(request_idx) > 0 else request_idx
        if request_idx != idx:
            return json.dumps({'error': 'idx_mismatch'})
        try:
            delete_vacancy(idx)
        except Exception as e:
            print(str(e))
            db_session.rollback()
            return json.dumps({'error': True})
        else:
            db_session.commit()
            return json.dumps({'success': url_for('vacancies_page')})

    vacancy = get_vacancy(idx)
    content = {'vacancy': vacancy, 'vacancy_name': str(vacancy)}
    return render_template('vacancy.html', **content)
