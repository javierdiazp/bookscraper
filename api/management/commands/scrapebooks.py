from django.core.management.base import BaseCommand, CommandError
from api.models import Category

import requests
from requests.exceptions import HTTPError
from requests.compat import urljoin
from bs4 import BeautifulSoup


class Command(BaseCommand):
    path = 'http://books.toscrape.com/'
    help = f'Obtiene las categorias y la informacion en detalle de los libros de {path}'

    def handle(self, *args, **options):
        try:
            categories = self.get_categories()
            for category in categories:
                c = Category(name=category['name'])
                # c.save()

                category_url = self.path + category['href']
                while category_url:
                    htmlparsed = self.get_html_parsed(category_url)
                    books = self.get_books(htmlparsed)
                    category_url = self.get_next_page(category_url, htmlparsed)

        except HTTPError as http_err:
            raise CommandError(f'Error en la peticion HTTP: {http_err}')
        except Exception as err:
            raise CommandError(f'Error: {err}')
        else:
            self.stdout.write(self.style.SUCCESS('Scraping finalizado correctamente'))

    def get_categories(self):
        response = requests.get(self.path)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        tags = soup.find(class_='side_categories').find_all('a')
        tags.pop(0)

        categories = []

        for tag in tags:
            categories.append({'name': tag.string.strip(), 'href': tag.get('href')})

        return categories

    @staticmethod
    def get_html_parsed(url):
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    @staticmethod
    def get_books(htmlparsed):
        books_uri = []
        for article in htmlparsed.find_all('article', class_='product_pod'):
            books_uri.append(article.find('a').get('href'))
        return books_uri

    @staticmethod
    def get_next_page(baseurl, htmlparsed):
        nextpage = htmlparsed.find('li', class_='next')
        if nextpage is None:
            return ""
        else:
            href = nextpage.find('a').get('href')
            return urljoin(baseurl, href)
