from abc import ABC, abstractmethod
import requests
import json


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
        url = f'https://api.hh.ru/vacancies?text={search_query}'
        response = requests.get(url)
        return response.json()


class Vacancy:
    """
    Class for saving info about vacancies, can be used for comparisons
    """

    def __init__(self, title, link, salary, description):
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description

class JSONSaver:
    """
    Class for working with json file
    """
    def __init__(self, filename):
        self.filename = filename

