python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

python .\add_user.py
python .\generate_description.py

# DO NOT USE
pip freeze > requirements.txt 