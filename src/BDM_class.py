import psycopg2


class BDManager:

    def __init__(self, host='localhost', database='hh data base', user='postgres', password='qwaszxL1',
                 keyword='python'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.keyword = keyword
        self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

    def get_companies_and_vacancies_count(self):
        """
        Get names of all employers and quantity of open vacancies
        :return: none
        """
        with self.conn.cursor() as cur:
            cur.execute("SELECT Название, Количество_открытых_вакансий FROM employers")
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_all_vacancies(self):
        """
        Get all vacancies, url, data about salary and company name
        :return: none
        """
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT vacancies.Название, vacancies.Ссылка, Минимальная_зарплата, Максимальная_зарплата,
            employers.Название AS Название_компании
            FROM vacancies
            LEFT JOIN employers USING (ID_компании)         
            """)

            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_avg_salary(self):
        """
        Get the average min salary ignoring vacancies in which information about min salary is not specified
        :return: none
        """
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT AVG(Минимальная_зарплата) FROM vacancies
            WHERE Минимальная_зарплата NOT IN (0)
            """)

            average_payment = cur.fetchall()
            print(average_payment)

    def get_vacancies_with_higher_salary(self):
        """
        Get vacancies' data with min salary higher than average salary
        :return: none
        """
        with self.conn.cursor() as cur:
            cur.execute(f"""
            SELECT * FROM vacancies
            WHERE Минимальная_зарплата > (SELECT AVG(Минимальная_зарплата) FROM vacancies)
            """)

            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_vacancies_with_keyword(self):
        """
        Get vacancies containing keyword in name of vacancy. Default keyword 'python', it can be changed at
        initialization of class's instance
        :return: none
        """
        with self.conn.cursor() as cur:
            cur.execute(f"""
            SELECT * FROM vacancies
            WHERE Название LIKE '%{self.keyword}%' OR Название LIKE '%{self.keyword.title()}%'
            """)

            rows = cur.fetchall()
            for row in rows:
                print(row)
