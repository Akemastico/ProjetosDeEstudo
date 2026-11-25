# 1. Apaga o banco
rm db.sqlite3

# 2. Apaga todas as migrations (exceto __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# 3. Cria migrations do zero
python manage.py makemigrations

# 4. Aplica tudo
python manage.py migrate   