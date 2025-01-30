setup: prepare install prepare-db

prepare: req
	cp -n .env.example .env

install:
	uv sync

prepare-db:
	uv run python manage.py migrate

serve:
	uv run python manage.py runserver 0.0.0.0:8000

shell:
	uv run python manage.py shell

lint:
	uv run ruff check .

update-locale:
	django-admin makemessages -l ru

compile-locales:
	django-admin compilemessages

test:
	uv run python manage.py test

test-coverage:
	uv run coverage run --source='.' manage.py test task_manager
	coverage html
	coverage report

req:
	uv pip export -f requirements.txt --output requirements.txt
