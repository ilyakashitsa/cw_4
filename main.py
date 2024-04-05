from src.hhapi import HeadHunterRuAPI
from src.seve_json_txt import SaveJson
from src.vacancy import VacanciesHH


def get_value(dictionary, *keys):
    """
    Возвращает значение из словаря по заданному пути ключей
    :param dictionary: словарь, из которого мы получаем значение
    :param keys: переменное количество ключей в виде строки, определяющих путь к значению.
    :return: Значение из словаря, связанное с заданным путем ключей.
     Если хотя бы один ключ не существует или путь прерывается значениями None, будет возвращено None.
    """
    for key in keys:
        if dictionary is None:
            return None
        dictionary = dictionary.get(key)
    return dictionary


def user_interaction():
    name_vacancy = input('Введите название вакансии: ')
    keyword_vacancy = input('Введите ключевые слова для фильтрации вакансий: ').split()

    vacancy_hh = HeadHunterRuAPI()
    all_vacancy = vacancy_hh.getting_vacancies(name_vacancy)

    all_vacancy = [vacancy for vacancy in all_vacancy.get('items') if get_value(vacancy, 'salary', 'currency') == 'RUR']

    if len(all_vacancy) == 0:
        print("По вашему запросу вакансий не найдено")
    else:
        print(f"Всего количество вакансий по запросу '{name_vacancy}': {len(all_vacancy)}")
        print(f"Топ {len(all_vacancy)} вакансий по зарплате:")

        good_vacancy = []

        if not keyword_vacancy:
            for vacancy in all_vacancy:
                try:
                    name = get_value(vacancy, 'name')
                    area = get_value(vacancy, 'area', 'name')
                    salary_from = get_value(vacancy, 'salary', 'from')
                    salary_to = get_value(vacancy, 'salary', 'to')
                    salary_currency = get_value(vacancy, 'salary', 'currency')
                    requirement = get_value(vacancy, 'snippet', 'requirement')
                    alternate_url = get_value(vacancy, 'alternate_url')
                    good_vacancy.append(
                        VacanciesHH(name, area, salary_from, salary_to, salary_currency, requirement, alternate_url))
                except Exception as e:
                    print(f"Ошибка обработки вакансии: {e}")
        else:
            for vacancy in all_vacancy:
                try:
                    name = get_value(vacancy, 'name')
                    area = get_value(vacancy, 'area', 'name')
                    salary_from = get_value(vacancy, 'salary', 'from')
                    salary_to = get_value(vacancy, 'salary', 'to')
                    salary_currency = get_value(vacancy, 'salary', 'currency')
                    requirement = get_value(vacancy, 'snippet', 'requirement')
                    alternate_url = get_value(vacancy, 'alternate_url')
                    if any(keyword.lower() in str(vacancy).lower() for keyword in keyword_vacancy):
                        good_vacancy.append(
                            VacanciesHH(name, area, salary_from, salary_to, salary_currency, requirement,
                                        alternate_url))
                except Exception as e:
                    print(f"Ошибка обработки вакансии: {e}")

        if len(good_vacancy) == 0:
            top_n_vacancy = len(all_vacancy)
            print(f"Ключевые слова не найдены. Будут выданы все результаты: {top_n_vacancy} вакансий.")
            good_vacancy = all_vacancy
        else:
            top_vacancy = sorted(good_vacancy, key=lambda x: x.salary_to if x.salary_to is not None else 0,
                                 reverse=True)
            good_vacancy = top_vacancy

        save_json = SaveJson('vacancies.json')

        save_json.add_vacancy(good_vacancy)
        save_json.save()

        print(good_vacancy)


if __name__ == "__main__":
    user_interaction()
