# digitalstudiocloud
Service providing API to catalog and store digital assets for creative purposes

For development testing:

``python -m venv <path to venv>``
``. <path to venv>/bin/activate``
``pip install -r dev-requirements.txt -r requirements.txt``
``uvicorn dsc.main:app --reload`` NOTE: will create ./sql_app.db sqlite database file
