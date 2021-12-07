install:
	pip3 install -r requirements.txt
freeze:
	pip3 freeze

env:
	virtualenv venv
		 
activate:
		source venv/bin/activate

deactivate:
		deactivate

shell:
	python3 manage.py shell

test:
	python3 manage.py test

run:
	python3 manage.py runserver

show:
	python3 manage.py showmigrations

migration:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

superuser:
	python3 manage.py createsuperuser

seed:
	python3 manage.py seed

unseed:
	python3 manage.py unseed

club_seed:
	python3 manage.py club_seed

club_unseed:
	python3 manage.py club_unseed

member_seed:
	python3 manage.py member_seed

member_unseed:
	python3 manage.py member_unseed

html: 
	coverage report
	coverage html

coverage:
	coverage run manage.py test
