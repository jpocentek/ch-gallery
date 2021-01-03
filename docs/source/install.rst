************
Installation
************

Clone repository to desired location::

   git clone git@github.com:jpocentek/ch-gallery.git

Install package::

   python setup.py develop

You may also install dev dependencies via PIP::

   pip install -r requirements-dev.txt

Install ``npm`` packages::

   npm install

Assets
######

To build static assets you have to install all packages with ``npm install`` and run::

   npm run build

or, if you want to get production-ready, minified and optimized files::

   npm run build-production

Run devserver
#############

The simplest way is to run Flask development server::

    $ export FLASK_APP=chgallery
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run
