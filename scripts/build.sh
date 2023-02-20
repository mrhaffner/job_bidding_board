cd job_bidding_board
rm contract_board/db.sqlite3
git pull origin main
pip install -r requirements.txt
cd contract_board/
rm -r static
python3 manage.py collectstatic
python3 manage.py makemigrations board
python3 manage.py migrate

python3 manage.py loaddata initial_data

touch /var/www/ics499_pythonanywhere_com_wsgi.py