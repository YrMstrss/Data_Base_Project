import requests


def get_employer_id(keyword: str) -> str:
    """
    Get id of the employer by company name.
    :param keyword: company name
    :return: employer id
    """

    params = {'text': keyword}
    request = requests.get('https://api.hh.ru/employers', params=params)

    return request.json()['items'][0]['id']
