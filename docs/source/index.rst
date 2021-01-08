.. CH Gallery documentation master file, created by
   sphinx-quickstart on Tue Dec 29 23:18:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CH Gallery
==========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   configuration

Simple gallery application using `Flask <https://github.com/pallets/flask>`_ and `SQLAlchemy <https://www.sqlalchemy.org/>`_
for backend.
Gallery page is made to be used with `PhotoSwipe <https://github.com/jpocentek/PhotoSwipe/>`_ script.

.. warning:: This is work in progress and it's not production-ready yet.

Requirements
############

* Python 3.5 or higher
* Python PIP (tested with 20.3.3 but older versions should also work)
* node.js with NPM (tested with NPM 6.14.10)

This repository uses Pillow for image manipulation so be sure to follow instructions for Pillow installation for your OS.
For now it has been tested only on Linux (Debian 9 and 10).

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
