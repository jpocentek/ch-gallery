# CH Gallery

![License: MIT](https://img.shields.io/github/license/commonality/readme-inspector.svg)

Simple gallery application using Flask and SQLAlchemy for backend. This is work in progress and it's not production-ready
yet.

## Requirements

* Python 3.5 or higher
* Python PIP (tested with 20.3.3 but older versions should also work)
* node.js with NPM (tested with NPM 6.14.10)

This repository uses Pillow for image manipulation so be sure to follow instructions for Pillow installation for your OS.
For now it has been tested only on Linux (Debian 9 and 10).

## Installation

Clone repository to desired location:
```
git clone git@github.com:jpocentek/ch-gallery.git
```

Install package:
```
python setup.py develop
```

You may also install dev dependencies via PIP:
```
pip install -r requirements-dev.txt
```

Install `npm` packages:
```
npm install
```

## Assets

To build static assets you have to install all packages from `package.json` and run
```
npm run build
```
or, if you want to get production-ready, minified and optimized files:
```
npm run build-production
```

## Run devserver

The simplest way is to run Flask development server:
```
export FLASK_APP=chgallery
export FLASK_ENV=development
flask init-db
flask run
```
