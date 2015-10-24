install:
	pip install -r requirements/dev.txt
	npm install

run: clean grunt runserver

runserver:
	python manage.py runserver

grunt:
	grunt &

test: clean
	py.test

clean:
	find . -name '*.pyc' -delete


makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate
