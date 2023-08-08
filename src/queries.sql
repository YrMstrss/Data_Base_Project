CREATE TABLE employers
(
	ID_компании int PRIMARY KEY,
	Название varchar(50),
	Ссылка varchar(50),
	Описание text,
	Город varchar(30),
	Количество_открытых_вакансий int
);

CREATE TABLE vacancies
(
	ID_вакансии int PRIMARY KEY,
	Название varchar(50),
	Ссылка varchar(50),
	Тип_занятости varchar(30),
	Город varchar(30),
	Опыт_работы varchar(20),
	Минимальная_зарплата int,
	Максимальная_зарплата int,
	Валюта varchar(3),
	ID_компании int REFERENCES empoyers (ID_компании) NOT NULL
)