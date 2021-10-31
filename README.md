# CoreAnalysis-backend
Backend-часть проекта. 

## Get started
```shell
pip install virtualenv
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
export FLASK_APP=backend
flask run
```

## Run tests
```shell
python -m pytest tests/
```

## Methods
**POST** `/api/report/`

Загрузка файла на сервер и получение отчёта по нему

*Input*: file

*Output*: JSON:
* `filename`: String

## API
[API](https://github.com/PracticeProject21/CoreAnalysis-backend/wiki/API)
