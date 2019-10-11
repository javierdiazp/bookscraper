from api.models import Category, Book
from rest_framework import viewsets
from api.serializers import CategorySerializer, BookSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ Lista de categorias """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """ Lista de libros """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
