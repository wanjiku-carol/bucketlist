# BucketList Application API

[![CircleCI](https://circleci.com/gh/wanjiku-carol/bucketlist.svg?style=svg)](https://circleci.com/gh/wanjiku-carol/bucketlist)

According to Merriam-Webster Dictionary, a Bucket List is a list of things that one has not done before but wants to do before dying.

## Installation and Setup

Clone the repo
>git clone https://github.com/wanjiku-carol/bucketlist.git

Navigate to the root folder

>cd bucketlist

Create the virtual environment

> mkvirtualenv blist-venv

Activate the virtual environment

>workon blist-venv

Install the requirements

>pip install -r requirements.txt

## Set Up Environment

Ensure that the app automatically sets up the environment variables to be used by adding them to the post-activate file of the virtual environment.
Open the virtual environment post-activate file

>atom $VIRTUAL_ENV/bin/postactivate

Add the environment set up in the post-activate file. Add the postgres server activation in the set up as well.

>pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start

>export FLASK_APP="run.py"

>export SECRET="b'\xf4u\x97\x1b\x9c\xf9\xe8\xff\xd8A\x92g\xaef\xea<\x9a>OBL\x9f\xb4q'"

>export APP_SETTINGS="development"

>export DATABASE_URL="postgresql://localhost/bucketlist_db"



 Re-activate your virtual environment.

 ## Run Database Migrations

Initialize, migrate, upgrade the database

>python manage.py db init

>python manage.py db migrate

>python manage.py db upgrade


## Launch the Progam

Run

>python run.py development

Interact with the API, send http requests using Postman

## API Endpoints
| URL Endpoint | HTTP Methods | Summary |
| -------- | ------------- | --------- |
| `/auth/register` | `POST`  | Register a new user|
|  `/auth/login` | `POST` | Login and retrieve token|
| `/bucketlists` | `POST` | Create a new Bucketlist |
| `/bucketlists` | `GET` | Retrieve all bucketlists for user |
| `/bucketlists/?page=1&limit=3` | `GET` | Retrieve three bucketlists per page |
 `/bucketlists/?q=name` | `GET` | searches a bucketlist by the name|
| `/bucketlists/<id>` | `GET` |  Retrieve a bucketlist by ID|
| `/bucketlists/<id>` | `PUT` | Update a bucketlist |
| `/bucketlists/<id>` | `DELETE` | Delete a bucketlist |
| `/bucketlists/<id>/items` | `POST` |  Create items in a bucketlist |
| `/bucketlists/<id>/items/<item_id>` | `DELETE`| Delete an item in a bucketlist|
| `/bucketlists/<id>/items/<item_id>` | `PUT`| update a bucketlist item details|

Run the APIs on postman to ensure they are fully functioning.

# Bucket List Front End

## Development server

>cd bucketlist

>cd blist-frontend

Run `ng install` to install the dependencies.

Run `ng serve --port 9000` for a dev server. Navigate to `http://localhost:9000/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `-prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).
Before running the tests make sure you are serving the app via `ng serve --port 9000`.
