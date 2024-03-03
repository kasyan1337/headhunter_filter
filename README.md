# Vacancy Filter Tool

## Overview

The Vacancy Filter Tool is a Python-based application designed to interact with the HeadHunter API to fetch, filter, and manage job vacancies. It allows users to search for vacancies using specific keywords, filter these vacancies based on salary requirements and keywords, and save the filtered list for further review. The tool is ideal for job seekers who want to streamline their job search process by focusing on vacancies that meet their specific criteria.

## Features

- **Fetch Vacancies**: Retrieve job vacancies from the HeadHunter API based on user-defined search queries.
- **Filter by Salary**: Filter the fetched vacancies based on a minimum salary requirement.
- **Filter by Keywords**: Further refine the list by filtering vacancies that include certain keywords in their descriptions.
- **Save Filtered Vacancies**: Save the filtered vacancies to a JSON file for easy access and review.

## How to Use

    python main.py


## Example input:

   ```
    Введите поисковый запрос: Python
    Введите сколько вакансии хотите посмотреть: 50 (MAX 50, INT ONLY)
   ```

2. **Filtering Vacancies**: After fetching the vacancies, you can filter them based on salary and keywords. You'll be prompted to enter a minimum salary and keywords (separated by commas).

    Example input:

    ```
    Введите количество вакансий для вывода в топ N: 10 (INT ONLY)
    Введите ключевые слова для фильтрации вакансий: Python, Django (KEYWORDS MUST BE DIVIDED BY COMMA AND SPACE ', ')
    Введите минимальную зарплату для фильтрации вакансий: 50000 (INT ONLY)
    ```

3. **Reviewing Filtered Vacancies**: The filtered vacancies will be saved to `database_filtered.json`. You can review this file directly or use additional functionality within the tool to display these vacancies in your console or terminal.

### Important Methods

- `filter_by_keyword(keywords)`: Filters the fetched vacancies by specified keywords.
- `filter_by_salary(salary_min)`: Filters the fetched vacancies by a minimum salary requirement.
- `show_filtered(top_n)`: Displays the top N filtered vacancies based on your criteria.

## File Structure

- `main.py`: The main script to run the tool.
- `classes.py`: Contains the core classes and methods for fetching, filtering, and managing vacancies.
- `data/database.json`: The default file where fetched vacancies are stored.
- `data/database_filtered.json`: The file where filtered vacancies are saved.