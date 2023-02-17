what folder is this being run from????

git pull origin main (cd first???)
pip install -r requirements.txt

cd contract_board (chained????)

rm db.sqlite3 (will this work if website is running?)
mkdir static
python3 manage.py collectstatic
python3 manage.py makemigrations board
python3 manage.py migrate


??? load initial data ???


??? reload app ???