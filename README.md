IHaveBeenDays
=============

[![Build Status](https://travis-ci.org/kplaube/ibeendays.svg?branch=master)](https://travis-ci.org/kplaube/ibeendays)
[![Coverage Status](https://coveralls.io/repos/kplaube/ibeendays/badge.svg?branch=master)](https://coveralls.io/r/kplaube/ibeendays?branch=master)

IHaveBeenDays (working title) is a web app that helps you tracking how many days
you have doing (or not doing) something. I'm building this application in order
to help me to control some manias, like nail biting or take too much coffee.


Why open source this?
---------------------

Why not? Creating a basic API that solves this problem allow us to develop a
lot of possibilities, like apps for wearables, browsers, smartphones, etc. If
you are out of ideias in your Hackathon, use our API :)

This project is strongly inspired by [Toggl](http://toggl.com).


Installing
----------

To install the project, you'll need the following tools:

* [Python 3.4.x](https://www.python.org/downloads/)
* [Node.js/NPM](https://nodejs.org/download/)
* [Grunt-cli](http://gruntjs.com/getting-started)
* [PostgresSQL](http://www.postgresql.org/download/)
* [Make](http://en.wikipedia.org/wiki/Make_(software))

It's possible to install pretty much all project's dependencies throught **Makefile**:

    $ make install

Remember: [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) is life.


Running
-------

You can serve the application throught **runserver** task, that will run the HTTP server throught [Gunicorn](http://gunicorn.org/):

    $ make runserver

Now you can access the service through **http://localhost:5000**.

For debugging purposes, you can run the [Django's built-in HTTP server](https://docs.djangoproject.com/en/1.7/ref/django-admin/#runserver-port-or-address-port) throught **manage.py**:

    $ python manage.py runserver


Developing
----------

We use Grunt to automate part of our flow. Grunt will help us compiling our SCSS and Javascript
(if needed):

    $ make grunt

To keep our lives easier, you can run all the project stack through **run** task:

    $ make run

It will run Grunt and the HTTP server.

Tests are essential! And we are trying to keep this step of development easy:

    $ make test

This task will run all project's test suit. So, before pushing your code, keep an eye on this guy.
