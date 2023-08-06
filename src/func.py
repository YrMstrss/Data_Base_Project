import requests


companies = ['Сбер. IT', 'Яндекс', 'Blue underlined link', 'Effective Mobile', 'Райффайзен Банк',
             'Ozon Информационные технологии', 'Ostrovok.ru', 'ПАО ВТБ, Технологический блок', 'Haraba',
             'VoxWeb Interactive', 'ТОО Playrix']


def get_employer_id(keyword: str) -> str:
    """
    Get id of the employer by company name.
    :param keyword: company name
    :return: employer id
    """

    params = {'text': keyword}
    request = requests.get('https://api.hh.ru/employers', params=params)

    return request.json()['items'][0]['id']


def get_employer_info(keyword: str) -> dict:
    """
    Get employee information by company name using get_employer_id function.
    :param keyword: company name
    :return: info about employer
    """

    employer_id = get_employer_id(keyword)
    request = requests.get(f'https://api.hh.ru/employers/{employer_id}')

    return request.json()


def get_employer_vacancies(emp_id: str) -> list[dict]:
    """
    Get info about python-vacancies of employer
    :param emp_id: employee id
    :return: list of dictionaries containing info about vacancies
    """
    params = {'text': 'python', 'page': 0, 'per_page': 100, 'employer_id': emp_id}
    request = requests.get('https://api.hh.ru/vacancies', params=params)

    data = request.json()['items']

    vacancies = []

    for item in data:
        vacancy = {
            'name': item['name'], 'url': item['alternate_url'], 'employment': item['employment']['name'],
            'area': item['area']['name']
        }

        if item['experience']['name'] == 'Нет опыта':
            vacancy['experience'] = 'Без опыта'
        elif item['experience']['name'] == 'От 1 года до 3 лет':
            vacancy['experience'] = 'От 1 года'
        elif item['experience']['name'] == 'От 3 до 6 лет':
            vacancy['experience'] = 'От 3 лет'
        elif item['experience']['name'] == 'Более 6 лет':
            vacancy['experience'] = 'От 6 лет'
        else:
            vacancy['experience'] = 'Не имеет значения'

        if item['salary'] is None:
            vacancy['min_salary'] = 'По договоренности'
            vacancy['max_salary'] = 'По договоренности'
            vacancy['currency'] = 'Не указано'
        else:
            if item['salary']['from'] is None:
                vacancy['min_salary'] = 'Минимальная зарплата не указана'
            else:
                vacancy['min_salary'] = item['salary']['from']

            if item['salary']['to'] is None:
                vacancy['max_salary'] = 'Максимальная зарплата не указана'
            else:
                vacancy['max_salary'] = item['salary']['to']
            if item['salary']['currency'] == 'RUR':
                vacancy['currency'] = 'RUB'
            else:
                vacancy['currency'] = item['salary']['currency']

        vacancies.append(vacancy)

    return vacancies
