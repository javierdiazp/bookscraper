import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

if __name__ == '__main__':
    try:
        response = requests.get('http://books.toscrape.com/index.html')
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'Error en la request HTTP: {http_err}')
    except Exception as err:
        print(f'Error: {err}')
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        categories = soup.find(class_='side_categories').find_all('a')
        categories.pop(0)

        for category in categories:
            print(category.string.strip())
