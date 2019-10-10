from django.core.management.base import BaseCommand, CommandError
from api.models import Category

import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Obtiene las categorias de libros de http://books.toscrape.com/'

    def handle(self, *args, **options):
        try:
            response = requests.get('http://books.toscrape.com/index.html')
            response.raise_for_status()
        except HTTPError as http_err:
            raise CommandError(f'Error en la request HTTP: {http_err}')
        except Exception as err:
            raise CommandError(f'Error: {err}')
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            categories = soup.find(class_='side_categories').find_all('a')
            categories.pop(0)

            for category in categories:
                c = Category(name=category.string.strip())
                c.save()

            self.stdout.write(self.style.SUCCESS('Scraping finalizado correctamente'))
