# TastyBackbonePie

Django helper classes to create ajax data tables with [backbone.js](http://backbonejs.org/) and [django-tastypie](http://tastypieapi.org/).
Includes a way to easily paginate, sort and filter tables too.

__Version 0.1 alpha - This project is in a very early stage.__

## Installation

### Requirements

Maybe it works with other versions too, but atm it is tested with:

- Django 1.5
- Tastypie 0.9.12

Install using pip:

```
pip install django==1.5 django-tastypie==0.9.12
```

### Install TastyBackbonePie

0. Using pip too:
	
	```
	pip install https://github.com/sspross/tastybackbonepie/zipball/master
	```

0. Add it to your `INSTALLED_APPS`:

	```
	INSTALLED_APPS = (
		...
		'tastybackbonepie',
		...
	)
	```

## How to use

### Tastypie example setup

0. Create a Tastypie API ressource e.g. `api.py` like:

	```
	from tastypie import fields
	from tastypie.resources import ModelResource
	from myapp.models import Book


	class BookResource(ModelResource):
	    class Meta:
	        queryset = Book.objects.all()
	        resource_name = 'book'
	        allowed_methods = ['get']
	        fields = ('id', 'name', 'added', 'read')
	```

0. Add to your `urls.py` file:

	```
	from tastypie.api import Api
	from myapp.api import BookResource


	v1_api = Api(api_name='v1')
	v1_api.register(BookResource())

	urlpatterns += patterns('',
	    (r'^api/', include(v1_api.urls)),
	)
	```

Now you should be able to access your ressource over your API like `/api/v1/book/?format=json`.

### Basic table

0. Use `TastyBackbonePieTableHelper` to define your table and add it to your views context:

	```
	from django.views.generic import TemplateView
	from tastybackbonepie.helpers import TastyBackbonePieTableHelper


	class BookTable(TastyBackbonePieTableHelper):
		uid = 'book_table'
	    root_url = '/api/v1/book/'
	    fields = [
	        {
	            'key': 'name',
	            'label': 'Name',
	        },
	    ]


	class TestView(TemplateView):
	    template_name = 'test.html'

	    def get_context_data(self, **kwargs):
	        context = super(TestView, self).get_context_data(**kwargs)
	        context['book_table'] = BookTable()
	        return context
	```


### HTML fields

### Additional HTML fields

### Column sorting

### Filtering