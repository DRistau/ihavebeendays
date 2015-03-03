install:
	pip install -r requirements/dev.txt
	pip install -r requirements/tests.txt
	npm install -g grunt-cli
	npm install

run: grunt runserver

runserver:
	foreman start

grunt:
	grunt &

test:
	py.test
