# testme

Quiz application built with Django. Mostly built to try out Django following a good experience using Flask.

### Planned features

- [ ] Create quizzes
- [ ] Add questions to quizzes
- [ ] Add time limits to quizzes and or individual questions
- [x] See results at the end of a quiz
- [ ] See stats for questions in a quiz to see how other users are doing
- [ ] Detailed view of your own stats
- [ ] Categorize quizzes
- [ ] Search for quizzes in a public database
- [ ] Create private quizzes with a shareable link

## Setup

These setup instructions assume you already have Python and [virtualenv](https://pypi.org/project/virtualenv/) installed. 

### 1. Install dependencies

The following will clone this repository, setup and activate a virtual environment, and install dependencies.

#### Windows

```shell script
git clone https://github.com/NeedsSoySauce/COMPSCI-235-A3.git
cd .\COMPSCI-235-A3\
virtualenv .virtualenv
.\.virtualenv\Scripts\activate
pip install -r requirements.txt
```

#### Mac OS / Linux

```shell script
git clone https://github.com/NeedsSoySauce/COMPSCI-235-A3.git
cd .\COMPSCI-235-A3\
virtualenv .virtualenv
source .\.virtualenv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup a local database

This will initialize a local sqlite3 database for development and testing.

```shell script
python manage.py makemigrations
python manage.py migrate
```

### 3. Create a superuser

The following will bring up a prompt where you can enter a username and password.

```shell script
python manage.py createsuperuser
```

## Execution

To start a development server:

````shell script
python manage.py runserver
```` 

## Testing

To run tests:

```shell script
python manage.py test
```

## Deployment

This project has not yet been deployed. **The secret key in settings.py is for development only**. If deploying to a production environment you should use environment variables (or some other system) that does not expose your secret key to the public.
