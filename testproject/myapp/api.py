from tastypie import fields
from tastypie.resources import ModelResource

from myapp.models import Book


class BookResource(ModelResource):
    class Meta:
        queryset = Book.objects.all()
        resource_name = 'book'
        allowed_methods = ['get']
        fields = ('id', 'name', 'added', 'read')
        #ordering = ('firstname', 'lastname', 'branch')
        #fields = ('id', 'firstname', 'lastname', 'birthday')
        #filtering = {
        #    'branch': ['exact'],
        #}