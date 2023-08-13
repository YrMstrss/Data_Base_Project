import psycopg2


class BDManager:

    def __init__(self, host='localhost', database='hh data base', user='postgres', password='qwaszxL1'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT Название, Количество_открытых_вакансий FROM employers")
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass
