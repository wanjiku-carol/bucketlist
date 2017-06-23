# BucketList Application API

According to Merriam-Webster Dictionary, a Bucket List is a list of things that one has not done before but wants to do before dying.

## Installation and Setup

>Clone the repo

https://github.com/r-wambui/bucket_list.git
Navigate to the root folder

>cd bucket_list
>Install the requirements

>pip install -r requirements.txt
>Initialize, migrate, upgrade the datatbase

>python manage.py db init
>python manage.py db migrate
>python manage.py db upgrade

## Launch the progam

Run

>python run.py

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

# Bucket List Front End

## Development server

Run `ng serve --port 9000` for a dev server. Navigate to `http://localhost:9000/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `-prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).
Before running the tests make sure you are serving the app via `ng serve`.
