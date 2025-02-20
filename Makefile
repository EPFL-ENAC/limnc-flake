install:
	poetry install

test:
	poetry run pytest -s

build:
	poetry build

clean:
	rm -rf dist

