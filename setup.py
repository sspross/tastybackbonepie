#! /usr/bin/env python
from setuptools import setup

import tastybackbonepie
setup(
    name='tastybackbonepie',
    version=tastybackbonepie.__version__,
    description='Django helper classes to create ajax data tables with backbone.js and django-tastypie.',
    long_description='Django helper classes to create ajax data tables with backbone.js and django-tastypie. Includes a way to easily paginate, sort and filter.',
    author='Silvan Spross',
    author_email='silvan.spross@gmail.com',
    url='http://github.com/sspross/tastybackbonepie/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=[
        'tastybackbonepie',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Communications :: Email',
    ],
    requires=[
    ],
    include_package_data=True,
)
