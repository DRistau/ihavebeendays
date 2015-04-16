install:
	pip install -r requirements/dev.txt
	npm install

run: grunt runserver

runserver:
	honcho start

grunt:
	grunt &

test:
	py.test
