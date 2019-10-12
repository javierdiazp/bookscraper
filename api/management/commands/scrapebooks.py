from django.core.management.base import BaseCommand, CommandError
from api.models import Category, Book

import re
import requests
from requests.exceptions import HTTPError
from requests.compat import urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class Command(BaseCommand):
    path = 'http://books.toscrape.com/'
    help = f'Get categories and detailed information of every book in {path}'

    def handle(self, *args, **options):
        try:
            categories = get_categories(self.path)
            with ThreadPoolExecutor() as executor:
                executor.map(self.thread_scrape_category, categories)
        except Exception as err:
            raise CommandError(f'Error: {err}')
        else:
            self.stdout.write(self.style.SUCCESS('Scraping completed'))

    def thread_scrape_category(self, category):
        c_name, c_url = category
        c = Category(name=c_name)
        c.save()

        while c_url:
            try:
                htmlparsed = get_html_parsed(c_url)
            except HTTPError:
                c_url = None  # Skip rest of category on http error
            else:
                books_url = get_books_url(c_url, htmlparsed)
                c_url = get_next_page(c_url, htmlparsed)

                for b_url in books_url:
                    try:
                        book_detail = get_book_detail(b_url)
                    except HTTPError:
                        pass  # Skip book on http error
                    else:
                        b = Book(category=c, **book_detail)
                        b.save()

        self.stdout.write(f'Category {c_name} successfully scraped')


def get_html_parsed(url):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'html.parser')


def get_categories(url):
    soup = get_html_parsed(url)
    category_tags = soup.find(class_='side_categories').find_all('a')
    category_tags.pop(0)  # First element is ignored (link to homepage)

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
    response.encoding = 'utf-8'

    book_detail = {}
    soup = BeautifulSoup(response.text, 'html.parser')

    # 'Product Main' Section
    product_main = soup.find(class_='product_main')
    if product_main:
        title = product_main.find('h1')
        if title:
            title = title.string
            book_detail['title'] = title
        else:
            raise HTTPError  # Storing a no named book has no meaning

        price = product_main.find(class_='price_color')
        if price:
            price = float(re.findall(r'\d+\.\d+', price.string)[0])
            book_detail['price'] = price

        stock = product_main.find('i', class_='icon-ok')
        stock = stock is not None
        book_detail['stock'] = stock
    else:
        raise HTTPError

    # 'Product Description' Section
    product_description = soup.find(id='product_description')
    if product_description:
        description = product_description.find_next_sibling('p')
        if description:
            description = description.string
            book_detail['product_description'] = description

    # Others
    thumbnail = soup.find(class_='thumbnail')
    if thumbnail:
        thumbnail = thumbnail.find('img').get('src')
        thumbnail = urljoin(url, thumbnail)
        book_detail['thumbnail_url'] = thumbnail

    upc = soup.find('th', string='UPC')
    if upc:
        upc = upc.find_next_sibling('td').string
        book_detail['upc'] = upc

    return book_detail
