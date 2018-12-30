# MTCE-py

## Installation

- `virtualenv -p python3 p3; source p3/bin/activate`

- `pip install -r requirements.txt`

- `python3 manage.py makemigrations`

- `python3 manage.py migrate`

## Usage

- `python3 manage.py runserver`

- open `http://127.0.0.1:8000/mtce/` in a browser


- `python3 manage.py background_importer [--workers 2]`

## Tests

- `python3 manage.py test`