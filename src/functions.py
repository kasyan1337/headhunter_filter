from src import classes as c


def user_interaction():
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
    print(f"Всего добавлено вакансий: {added_vacancies_count}.")

    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    # salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000
    #
    # filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    #
    # ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    #
    # sorted_vacancies = sort_vacancies(ranged_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)
