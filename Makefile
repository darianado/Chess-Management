install:
	pip3 install -r requirements.txt
freeze:
	pip3 freeze

env:
	virtualenv venv
		 

deactivate:
		deactivate

shell:
	python3 manage.py shell

test:
	python3 manage.py test

run:
	python3 manage.py runserver

show:
	python manage.py showmigrations

migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

seed:
	python manage.py seed

unseed:
	python manage.py unseed

clubs_seed:
	python manage.py club_seed

clubs_unseed:
	python manage.py club_unseed

member_seed:
	python manage.py member_seed

member_unseed:
	python manage.py member_unseed
