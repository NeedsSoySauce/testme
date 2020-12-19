# testme

Quiz application backend built with Django. Mostly built to try out Django following a good experience using Flask.

### Planned features

- [x] Create quizzes
- [x] Add questions to quizzes
- [ ] Add time limits to quizzes and or individual questions
- [ ] See results at the end of a quiz
- [ ] See stats for questions in a quiz to see how other users are doing
- [ ] Detailed view of your own stats
- [x] Categorize quizzes
- [ ] Search for quizzes in a public database
- [ ] Create private quizzes with a shareable link
- [x] Setup loading of keys from environment variables

## Setup

These setup instructions assume you already have Python and [virtualenv](https://pypi.org/project/virtualenv/) installed. 

### 1. Install dependencies

The following will clone this repository, setup and activate a virtual environment, and install dependencies.

#### Windows

```shell script
git clone https://github.com/NeedsSoySauce/testme.git
cd .\testme\
virtualenv .virtualenv
.\.virtualenv\Scripts\activate
pip install -r requirements.txt
```

#### Mac OS / Linux

```shell script
git clone https://github.com/NeedsSoySauce/testme.git
cd .\testme\
virtualenv .virtualenv
source .\.virtualenv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup a local database

This will initialize a local sqlite3 database for development and testing.

```shell script
python manage.py migrate
```

### 3. Create a superuser (optional)

The following will bring up a prompt where you can enter a username and password.

```shell script
python manage.py createsuperuser
```

#### Configure environment variables

The *.env* file at the project's root contains the following Django settings. Check the [Django documentation](https://docs.djangoproject.com/en/3.1/ref/settings/) for an explanation on what they do.

* `DEBUG`
* `SECRET_KEY`
* `TIME_ZONE`
* `LANGUAGE_CODE`

## Execution

To start a development server:

````shell script
python manage.py runserver
```` 

## Testing

This project uses Django's default testing suite `unittest`. Experience with it so far suggests moving to `pytest` could be worthwhile.

To run tests:

```shell script
python manage.py test
```
