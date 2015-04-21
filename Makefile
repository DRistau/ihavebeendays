install:
	pip install -r requirements/dev.txt
	npm install

run: clean grunt runserver

runserver:
	honcho start

grunt:
	grunt &

test: clean
	py.test

clean:
	find . -name '*.pyc' -delete
