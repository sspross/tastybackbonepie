# TastyBackbonePie

Django helper classes to create ajax data tables with backbone.js and django-tastypie. Includes a way to easily paginate, sort and filter tables too.

__Version 0.1 alpha - This project is in a very early stage.__

## Installation

### Requirements

Maybe it works with other versions too, but atm it is tested with:

- Django 1.5
- Tastypie 0.9.12

Install over pip

```
pip install django==1.5 django-tastypie==0.9.12
```

### Install TastyBackbonePie

0. Over pip too
	
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

### django-tastypie Setup

### Basic table