## Requirements

Installed [Python](http://python.org/) and [Virtualenv](http://pypi.python.org/pypi/virtualenv). See [this guide](http://install.python-guide.org/) for guidance.

## Installation

```
git clone git://github.com/sspross/tastybackbonepie.git
cd tastybackbonepie/tastybackbonepie/
mkvirtualenv djangoproject
pip install -r REQUIREMENTS
./manage.py syncdb
./manage.py runserver
```

Open in your browser: [http://localhost:8000/](http://localhost:8000/)