from src import classes as c


def load_database():
    hh_api = c.HeadHunterAPI()
    search_query = input("Введите поисковый запрос: ")

    try:
        number_of_vacancies = int(input("Введите сколько вакансии хотите посмотреть: "))
    except ValueError:
        print("Пожалуйста, введите число.")
        return

    hh_vacancies_json = hh_api.get_vacancies(search_query)
    vacancies_list = c.Vacancy.cast_to_object_list(hh_vacancies_json)

    added_vacancies_count = 0  # Counter for added vacancies
    json_saver = c.JSONSaver()

    for vacancy in vacancies_list[:number_of_vacancies]:  # limits the number of vacancies to add based on user input
        json_saver.add_vacancy(vacancy)
        added_vacancies_count += 1
        print(f"Вакансия номер {added_vacancies_count} '{vacancy.title}' добавлена в файл.")
    print(f"По запросу {search_query} было добавлено {added_vacancies_count} вакансий в избранные.")


def filter_database():
    json_saver = c.JSONSaver()  # Create an instance of JSONSaver

    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ")

    try:
        salary_min = int(
            input("Введите минимальную зарплату для фильтрации вакансий: "))  # Changed to just minimum for simplicity
    except ValueError:
        print("Пожалуйста, введите число.")
        return

    json_saver.filter_by_salary(salary_min)
    json_saver.filter_by_keyword(filter_words)
    print("Filtered vacancies by salary and keywords:")
    json_saver.show_filtered(top_n)
