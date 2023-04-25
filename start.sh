PY=python3.11

$PY -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
flask run
