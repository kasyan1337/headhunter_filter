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

    def get_vacancies(self, search_query):
        url = f'https://api.hh.ru/vacancies?text={search_query}&per_page=50'
        response = requests.get(url)
        return response.json()['items']


class Vacancy:
    """
    Class for saving info about vacancies, can be used for comparisons
    """

    def __init__(self, title, link, salary, description):
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description

    @staticmethod
    def cast_to_object_list(vacancies_json):
        return [Vacancy(v['name'], v['alternate_url'], v.get('salary', 'Не указана'), v['snippet']['requirement']) for v
                in vacancies_json]


class JSONSaver:
    """
    Class for working with json file
    """

    def __init__(self, filename='data/database_all.json'):
        self.filename = filename

    def load_database(self):
        """
        Load and display the entire database from database_all.json.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print("Database file not found.")
            return []
        except json.JSONDecodeError:
            print("Database file is empty or corrupted.")
            return []

    def dump_database(self, data):
        """
        Overwrite the entire database in database_all.json with new data.
        """
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f'Something went wrong saving database: {e}')

    def add_vacancy(self, vacancy):
        """
        Add a vacancy to database_favourite.json.
        The vacancy parameter in add_vacancy and delete_vacancy methods is expected to be a dictionary representing a vacancy.
        Ensure the dictionary includes a 'link' key for identification.
        """
        filepath = "data/database_favourite.json"
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

    def delete_vacancy(self, vacancy):
        """
        Delete a vacancy from database_favourite.json.
        The vacancy parameter in add_vacancy and delete_vacancy methods is expected to be a dictionary representing a vacancy.
        Ensure the dictionary includes a 'link' key for identification.
        """
        filepath = "data/database_favourite.json"
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
