import requests
import psycopg2


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
            'area': item['area']['name'], 'vacancy_id': item['id'], 'employer_id': emp_id
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
            vacancy['min_salary'] = 0
            vacancy['max_salary'] = 0
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


def add_employer_to_table(employer_dict: dict):
    """
    Add info about employer to database table
    :param employer_dict: dict with info about employer
    :return: none
    """
    with psycopg2.connect(host='localhost', database='hh data base', user='postgres', password='qwaszxL1') as conn:
        with conn.cursor() as cur:
            company_id = employer_dict['id']
            name = employer_dict['name']
            url = employer_dict['alternate_url']
            description = employer_dict['description']
            city = employer_dict['area']['name']
            vacancy_count = employer_dict['open_vacancies']
            cur.execute('INSERT INTO employers VALUES (%s, %s, %s, %s, %s, %s)', (company_id, name, url, description,
                                                                                  city, vacancy_count))
