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

Selenium?

## Git Workflow

To work on a new feature, keep things simple by starting from a new empty folder outside of the directory of any previous work (do not use your code from previous work)

Get the code from the main branch:

```sh
$ git clone https://github.com/mrhaffner/job_bidding_board.git
```

Create/switch to a new feature branch for the code you are working on (do not include "<>"):

```sh
$ git checkout -b <name-of-your-feature-branch>
```

Now it is time to work on your code!

To save your progress to the local git repository:

```sh
$ git add .
$ git commit -m "<a-short-statement-about-what-you-are-adding>"
```

This will add/commit all files in your current directory, you may replace "." with individuals files or folders.

Push your saved progress from local git repo to the remote git repo (where other people can see):

```sh
$ git push origin <name-of-your-feature-branch>
```

When you have finished work on your feature and you are sure everything is correct - it is time to submit a pull request to merge it with the main branch:

You can do this at https://github.com/mrhaffner/job_bidding_board

- Click on the pull requests tab
- Click on the "Create pull request" button
- Select your branch from the drop-down menu beginning with "compare:"
- Click "Create pull request" button
- Write a concise comment about what you are trying to merge
- Click "Create pull request" button

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
