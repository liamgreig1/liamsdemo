upgrade:
	pip-compile --upgrade

install:
	pip install .

install-dev:
	pip install -e .[dev]

test:
	flake8 && pytest

black:
	black .

coverage:
	coverage run -m --source=app pytest && coverage xml && coverage report -m

run:
	uvicorn app.main:app

run-dev:
	uvicorn app.main:app --reload
