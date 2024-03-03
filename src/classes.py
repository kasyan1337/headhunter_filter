import json
from abc import ABC, abstractmethod

import requests


class VacancyAPI(ABC):
    """
    In case diff platforms are needed in the future
    """

    @abstractmethod
    def get_vacancies(self, search_query):
        pass


class HeadHunterAPI(VacancyAPI):
    """
    Class for work with HH API
    """

    def get_vacancies(self, search_query: str):
        url = f'https://api.hh.ru/vacancies?text={search_query}&per_page=50'
        response = requests.get(url)
        return response.json()['items']


class Vacancy:
    """
    Class for filtering vacancies and comparisons
    """

    def __init__(self, title: str, link: str, salary: dict, description: str):
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description

    def __str__(self) -> str:
        return f"{self.title} ({self.link})"

    @staticmethod
    def cast_to_object_list(vacancies_json):
        return [Vacancy(v['name'], v['alternate_url'], v.get('salary', 'Не указана'), v['snippet']['requirement']) for v
                in vacancies_json]


class JSONSaver:
    """
    Class for loading the database
    """

    def __init__(self, filename='data/database.json'):
        self.filename = filename

    def add_vacancy(self, vacancy):
        """
        Add a vacancy to database.json.
        """
        filepath = "data/database.json"
        try:
            with open(filepath, 'r+', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []

                vacancy_dict = {
                    "title": vacancy.title,
                    "link": vacancy.link,
                    "salary": vacancy.salary,
                    "description": vacancy.description
                }

                data.append(vacancy_dict)
                file.seek(0)  # moves the file pointer to the beginning of the file
                file.truncate()  # trims the remaining part, makes the file smaller
                json.dump(data, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump([vacancy_dict], file, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy, filepath):
        """
        Delete a vacancy from database.json.
        """
        try:
            with open(filepath, 'r+', encoding='utf-8') as file:
                data = json.load(file)
                data = [v for v in data if v['link'] != vacancy['link']]
                file.seek(0)
                file.truncate()
                json.dump(data, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            print("Favourites database file not found.")
        except json.JSONDecodeError:
            print("Favourites database file is empty or corrupted.")

    def filter_by_salary(self, salary_min: int):
        """
        Filter out vacancies in database.json by salary and drop them in database_filtered.json
        """
        with open("data/database.json", 'r', encoding='utf-8') as file:
            vacancies = json.load(file)

        filtered_vacancies = [vacancy for vacancy in vacancies if
                              vacancy["salary"] and vacancy["salary"]["from"] and vacancy["salary"][
                                  "from"] >= salary_min]

        with open("data/database_filtered.json", 'w', encoding='utf-8') as file:
            json.dump(filtered_vacancies, file, ensure_ascii=False, indent=4)

    def filter_by_keyword(self, keywords: str):
        """
        Filter out vacancies in database_filtered.json bz keywords, if not delete instance
        Keywords must be separated by comma and space
        """
        with open("data/database_filtered.json", 'r+', encoding='utf-8') as file:
            vacancies = json.load(file)
            keywords = [keyword.strip().lower() for keyword in keywords.split(', ')]

        vacancies_to_remove = [vacancy for vacancy in vacancies if vacancy['description'] and not all(
            keyword in vacancy['description'].lower() for keyword in keywords)]

        for vacancy in vacancies_to_remove:
            self.delete_vacancy(vacancy, "data/database_filtered.json")

    def show_filtered(self, top_n: int):
        """
        Show filtered vacancies in database_filtered.json
        """
        try:
            with open("data/database_filtered.json", 'r', encoding='utf-8') as file:
                vacancies = json.load(file)

                # If list size exceeded, it shows the max amount
                vacancies_to_show = vacancies[:top_n]

                for vacancy in vacancies_to_show:
                    print(f"Title: {vacancy['title']}\n"
                          f"Salary: From {vacancy['salary']['from']} to {vacancy['salary']['to']} {vacancy['salary']['currency']}\n"
                          f"Description: {vacancy['description']}\nLink: {vacancy['link']}\n")
                if top_n <= len(vacancies):
                    print(f"Shown up to {top_n} vacancies out of {len(vacancies)} available.")

        except FileNotFoundError:
            print("Filtered database file not found.")
        except json.JSONDecodeError:
            print("Filtered database file is empty or corrupted.")
