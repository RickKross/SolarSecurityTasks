from task_1.app.models import Vacancies


def get_vacancies_list(page=None, page_length=None):
    result = Vacancies.query.order_by(Vacancies.name).all()
    if page and page_length:
        result = result.offset((page - 1) * page_length).limit(page_length)

    return list(result)


def get_vacancy(idx):
    result = Vacancies.query.filter_by(id=idx).first()
    return result


def delete_vacancy(idx):
    Vacancies.query.filter_by(id=idx).delete()
    return None

