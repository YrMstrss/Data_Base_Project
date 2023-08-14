import requests
import psycopg2


def get_employer_id(keyword: str) -> str:
    """
    Get id of the employer by company name.
    :param keyword: company name
    :return: employer id
    """

    params = {'text': keyword}
    request = requests.get('https://api.hh.ru/employers', params=params)

    if len(request.json()['items']) > 1:
        for item in request.json()['items']:
            if item['name'] == keyword:
                return item['id']

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
                vacancy['min_salary'] = 0
            else:
                vacancy['min_salary'] = item['salary']['from']

            if item['salary']['to'] is None:
                vacancy['max_salary'] = 0
            else:
                vacancy['max_salary'] = item['salary']['to']
            if item['salary']['currency'] == 'RUR':
                vacancy['currency'] = 'RUB'
            else:
                vacancy['currency'] = item['salary']['currency']

        vacancies.append(vacancy)

    return vacancies


def create_database(database_name: str, params: dict) -> None:
    """
    Create a database with given name and params
    :param database_name: Database name
    :param params: Parameters for connection to database
    :return: None
    """
    with psycopg2.connect(database='postgres', **params) as conn:
        with conn.cursor() as cur:
            cur.execute(f'DROP DATABASE {database_name}')
            cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    with psycopg2.connect(database=database_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    Company_ID int PRIMARY KEY,
                    Company_name varchar(50),
                    URL varchar(50),
                    Description text,
                    City varchar(30),
                    Vacancies_counter int
                    );
                    
                CREATE TABLE vacancies (
                    Vacancy_ID int PRIMARY KEY,
                    Vacancy_name varchar(100),
                    URL varchar(100),
                    Employment varchar(30),
                    City varchar(30),
                    Experience varchar(20),
                    Min_salary int,
                    Max_salary int,
                    Currency varchar(10),
                    Company_ID int REFERENCES employers (ID_компании) NOT NULL
                    )
            """)

    conn.close()


def add_employer_to_table(employer_dict: dict, database_name: str, params: dict) -> None:
    """
    Add info about employer to database table
    :param employer_dict: dict with info about employer
    :param database_name: Name of the database
    :param params: Parameters for connection to database
    :return: None
    """
    with psycopg2.connect(database=database_name, **params) as conn:
        with conn.cursor() as cur:
            company_id = employer_dict['id']
            name = employer_dict['name']
            url = employer_dict['alternate_url']
            description = employer_dict['description']
            city = employer_dict['area']['name']
            vacancy_count = employer_dict['open_vacancies']
            cur.execute('INSERT INTO employers VALUES (%s, %s, %s, %s, %s, %s)', (company_id, name, url, description,
                                                                                  city, vacancy_count))


def add_vacancy_to_table(vacancy_list: list, database_name: str, params: dict) -> None:
    """
    Add info about vacation to table
    :param vacancy_list: List with all vacations of employer
    :param database_name: Name of the database
    :param params: Parameters for connection to database
    :return: None
    """
    with psycopg2.connect(database=database_name, **params) as conn:
        with conn.cursor() as cur:
            for vacancy in vacancy_list:
                vacancy_id = vacancy['vacancy_id']
                name = vacancy['name']
                url = vacancy['url']
                employment = vacancy['employment']
                city = vacancy['area']
                experience = vacancy['experience']
                min_salary = int(vacancy['min_salary'])
                max_salary = int(vacancy['max_salary'])
                currency = vacancy['currency']
                employer_id = vacancy['employer_id']
                cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                            (vacancy_id, name, url, employment,
                             city, experience, min_salary, max_salary, currency, employer_id))


def clear_tables(database_name: str, params: dict):
    """
    Delete all info from tables 'employers' and 'vacancies'
    :return: None
    """
    with psycopg2.connect(database=database_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE employers, vacancies')
