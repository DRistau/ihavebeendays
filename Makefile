.PHONY: build clean help makemigrations migrate run runserver setup test

help:
	@echo
	@echo 'IHaveBeenDays'
	@echo
	@echo 'build .................................. Build assets'
	@echo 'help ................................... This screen :)'
	@echo 'makemigrations ......................... Create Django migrations'
	@echo 'migrate ................................ Run Project migrations'
	@echo 'run .................................... Build assets and run the project'
	@echo 'runsever ............................... Run web server'
	@echo 'setup .................................. Set the project ready to run'
	@echo 'test ................................... Run tests'
	@echo

setup: _install_python_dependencies _install_node_dependencies makemigrations migrate

run: clean build runserver

build:
	grunt &

clean:
	find . -name '*.pyc' -delete

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

runserver:
	python manage.py runserver

test: clean
	py.test ./ihavebeendays/


_install_python_dependencies:
	pip install -r requirements/dev.txt

_install_node_dependencies:
	npm install
