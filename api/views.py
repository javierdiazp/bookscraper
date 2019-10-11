from api.models import Category, Book
from rest_framework import viewsets
from api.serializers import CategorySerializer, BookSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ Categorias de libros """
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """ Libros de la web http://books.toscrape.com """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
