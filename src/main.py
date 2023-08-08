from src.func import get_employer_info, get_employer_vacancies, add_employer_to_table, add_vacancy_to_table


def main():
    companies = ['Сбер. IT', 'Яндекс', 'Blue underlined link', 'Effective Mobile', 'Райффайзен Банк',
                 'Ozon Информационные технологии', 'Ostrovok.ru', 'ПАО ВТБ, Технологический блок', 'Haraba',
                 'VoxWeb Interactive', 'ТОО Playrix']

    employer_ids = []

    for company in companies:
        company_info = get_employer_info(company)
        employer_ids.append(company_info['id'])
        add_employer_to_table(company_info)

    for employer_id in employer_ids:
        vacation_list = get_employer_vacancies(employer_id)
        add_vacancy_to_table(vacation_list)


if __name__ == '__main__':
    main()
