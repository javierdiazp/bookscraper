from django.core.management.base import BaseCommand, CommandError
from api.models import Category

import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Obtiene la informacion en detalle de los libros de http://books.toscrape.com/'

    def handle(self, *args, **options):
        pass
