class VacanciesHH:
    """
    Класс для представления вакансий
    """

    def __init__(self, name, city, salary_from, salary_to, currency, requirements, link):
        self.name = name
        self.city = city
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.requirements = requirements
        self.link = link

    def validate_data(self):
        """
        Валидация данный о вакансии
        :return: Если зарплата не указана, устанавливает значение 0 для salary_from.
        """
        if not self.salary_from and not self.salary_to:
            self.salary_from = 0

    def __lt__(self, other):
        """
        Метод для сравнения вакансий по ЗП
        :param other:
        :return: True, если зарплата текущей вакансии (self) меньше зарплаты второй вакансии (other)
        """
        return self.salary_from < other.salary_from

    def __eq__(self, other):
        """
        Проверка равенства вакансий
        :param other:
        :return: True, если атрибуты двух вакансий (self и other) равны
        """
        return (self.name == other.name and self.city == other.city and self.salary_from == other.salary_from
                and self.salary_to == other.salary_to
                and self.requirements == other.requirements and self.link == other.link)

    def __repr__(self):
        """
        Строковое представление объекта класса VacanciesHH
        :return:
        """
        return (f"""
                Название вакансии: {self.name}
                Город: {self.city}
                Заработная плата: {self.salary_from} - {self.salary_to} {self.currency}
                Требования: {self.requirements}
                Ссылка на вакансию: {self.link}
                """)

    @staticmethod
    def convert_to_dict(obj):
        """
        Сериализирует объект класса VacanciesHH в формат JSON.
        :param obj: объект класса VacanciesHH
        :return: словарь с атрибутами объекта
        """
        if isinstance(obj, VacanciesHH):
            return obj.__dict__
        return obj
