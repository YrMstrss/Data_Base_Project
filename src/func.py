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
    employer_id = get_employer_id(keyword)
    request = requests.get(f'https://api.hh.ru/employers/{employer_id}')

    return request.json()
