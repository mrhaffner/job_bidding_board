## Project Setup for Local Development

Install Python 3.10.x
Make sure to add Python to PATH.
Python will likely come with pip3.

Git steps: Clone the repo
cd into repo

Setup virtual environment

```sh
python3 -m venv env
```

Activate virtual environment:

From the job_bidding_board directory:

```sh
$ source env/bin/activate
```

Install the required python packages via pip

```sh
pip install -r requirements.txt
```

You will also need to install SQLite3

Installing Selenium (for functional tests)

On Mac, you will need to give it one time permission to run. Run this from the folder it is in.

```sh
$ xattr -d com.apple.quarantine chromedriver
```

## Python Style Guide

PascalCase for classes
snake_case for everything else

use single quotes for everything but docstrings

double space between top level functions and classes

## Run Development App

from the job_bidding_board directory:

```sh
$ source env/bin/activate
```

cd into the outer contract_board directory

run the app

```sh
python manage.py runserver
```

if you have updated the model, you will likely have to update the database:

```sh
$ python3 manage.py makemigrations board
$ python3 mange.py migrate
```
