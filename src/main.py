from src.func import get_employer_info, get_employer_vacancies, add_employer_to_table, add_vacancy_to_table,\
    clear_tables, create_database
from src.BDM_class import BDManager
from src.config import config


def main():
    companies = ['Сбер. IT', 'Яндекс', 'Blue underlined link', 'Effective Mobile', 'Райффайзен Банк',
                 'Ozon Информационные технологии', 'Ostrovok.ru', 'ПАО ВТБ, Технологический блок', 'Haraba',
                 'VoxWeb Interactive', 'ТОО Playrix']

    database_name = 'hh'
    employer_ids = []

    params = config()

    create_database(database_name, params)

    clear_tables(database_name, params)

    for company in companies:
        company_info = get_employer_info(company)
        employer_ids.append(company_info['id'])
        add_employer_to_table(company_info, database_name, params)

    for employer_id in employer_ids:
        vacation_list = get_employer_vacancies(employer_id)
        add_vacancy_to_table(vacation_list, database_name, params)

    db = BDManager()
    db.get_companies_and_vacancies_count()
    db.get_all_vacancies()
    db.get_avg_salary()
    db.get_vacancies_with_higher_salary()
    db.get_vacancies_with_keyword()


if __name__ == '__main__':
    main()
