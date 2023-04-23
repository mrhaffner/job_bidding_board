## Project Setup for Local Development

Install Python 3.10.x

Install Git

Install SQLite3

Make sure to add Python to PATH.

If you are on Windows, use GitBash (comes with Git installation)

Get the repo and move into it's directory:

```sh
$ git clone https://github.com/mrhaffner/job_bidding_board.git
$ cd job_bidding_board
```

Setup virtual environment

```sh
$ python -m venv env
```

Activate virtual environment (you may have to do this again in the future, always check your environment is running):

Mac/Linux:

```sh
$ source env/bin/activate
```

Windows:

```sh
$ source env/Scripts/activate
```

Install the required python packages via pip (you may have to reinstall if new version of the repo add dependencies)

```sh
$ pip install -r requirements.txt
```

## Run Development App

cd into the outer contract_board directory

Set up the database if it is not already set up:

```sh
$ python manage.py makemigrations board
$ python manage.py migrate
```

Run the app

```sh
$ python manage.py runserver
```

## Testing the App

You will need to install a ChromeDriver with a version matching your current version of Chrome. There are a number of ways to handle this, so you should look into driver installation on your own.

If you run the functional tests from a Linux machine, it will install Chromium drivers to your computer for you. This is meant for the Github Actions VM. It is not recommended to run the tests from a personal Linux machine at this moment.

On Mac, you will need to give it one time permission to run. Run this from the folder it is in.

```sh
$ xattr -d com.apple.quarantine chromedriver
```

You can only run the functional tests while the server is running and must flush the database first:

```sh
$ python manage.py test
```

Run the linter

```sh
$ flake8
```

### Interacting with the Database

If you have updated the model, you will likely have to update the database tables:

```sh
$ python manage.py makemigrations board
$ python manage.py migrate
```

Will load initial data for the application

```sh
$ python manage.py loaddata dump.json
```

Save database to JSON file

```sh
$ python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > dump.json
```

Remove all data from the database

```sh
$ python manage.py flush
```

### Create Super User

```sh
$ python manage.py createsuperuser
```
