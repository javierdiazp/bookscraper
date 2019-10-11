from django.core.management.base import BaseCommand, CommandError
from api.models import Category, Book

import re
import requests
from requests.exceptions import HTTPError
from requests.compat import urljoin
from bs4 import BeautifulSoup


class Command(BaseCommand):
    path = 'http://books.toscrape.com/'
    help = f'Obtiene las categorias y la informacion en detalle de los libros de {path}'

    def handle(self, *args, **options):
        try:
            categories = get_categories(self.path)
            for category in categories:
                c_name, c_url = category
                c = Category(name=c_name)
                c.save()

                while c_url:
                    htmlparsed = get_html_parsed(c_url)
                    books_url = get_books_url(c_url, htmlparsed)
                    c_url = get_next_page(c_url, htmlparsed)

                    for b_url in books_url:
                        book = get_book_detail(b_url)
                        b = Book(category=c, **book)
                        b.save()

                print(f'Categoria {c_name} analizada')

        except HTTPError as http_err:
            raise CommandError(f'Http Request Error: {http_err}')
        except Exception as err:
            raise CommandError(f'Error: {err}')
        else:
            self.stdout.write(self.style.SUCCESS('Scraping finalizado correctamente'))


def get_html_parsed(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def get_categories(url):
    soup = get_html_parsed(url)
    category_tags = soup.find(class_='side_categories').find_all('a')
    category_tags.pop(0)

    categories = []

    for tag in category_tags:
        categories.append((tag.string.strip(), urljoin(url, tag.get('href'))))

    return categories


def get_books_url(baseurl, htmlparsed):
    books_url = []
    for article in htmlparsed.find_all('article', class_='product_pod'):
        href = article.find('a').get('href')
        books_url.append(urljoin(baseurl, href))
    return books_url


def get_next_page(baseurl, htmlparsed):
    nextpage = htmlparsed.find('li', class_='next')
    if nextpage is None:
        return None
    else:
        href = nextpage.find('a').get('href')
        return urljoin(baseurl, href)


def get_book_detail(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Seccion 'Product Main'
    product_main = soup.find(class_='product_main')
    if product_main:
        title = product_main.find('h1')
        if title:
            title = title.string

        price = product_main.find(class_='price_color')
        if price:
            price = float(re.findall(r'\d+\.\d+', price.string)[0])

        stock = product_main.find('i', class_='icon-ok')
        stock = stock is not None
    else:
        title = price = stock = None

    # Seccion 'Product Description'
    product_description = soup.find(id='product_description')
    if product_description:
        description = product_description.find_next_sibling('p')
        if description:
            description = description.string
    else:
        description = None

    # Otros
    thumbnail = soup.find(class_='thumbnail')
    if thumbnail:
        thumbnail = thumbnail.find('img').get('src')

    upc = soup.find('th', string='UPC')
    if upc:
        upc = upc.find_next_sibling('td').string

    return {
        'title': title.string,
        'thumbnail_url': thumbnail,
        'price': price,
        'stock': stock,
        'product_description': description,
        'upc': upc
    }
