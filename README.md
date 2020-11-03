# testme

Quiz application built with Django. Mostly built to try out Django following a good experience using Flask in a previous project.

### Planned features

- [ ] Create quizes
- [ ] Add questions to quizes
- [ ] Add time limits to quizes and or individual questions
- [ ] See results at the end of a quiz
- [ ] See stats for questions in a quiz to see how other users are doing
- [ ] See stats for user on their own
- [ ] Categorize quizes
- [ ] Search for quizes in a public database
- [ ] Create private quizes with a shareable link

## Setup

These setup instructions assume you already have Python and [virtualenv](https://pypi.org/project/virtualenv/) installed. The following will clone this repository, setup and activate a virtual environment, and install dependencies.

### Windows

```shell script
git clone https://github.com/NeedsSoySauce/COMPSCI-235-A3.git
cd .\COMPSCI-235-A3\
virtualenv .virtualenv
.\.virtualenv\Scripts\activate
pip install -r requirements.txt
```

### Mac OS / Linux

```shell script
git clone https://github.com/NeedsSoySauce/COMPSCI-235-A3.git
cd .\COMPSCI-235-A3\
virtualenv .virtualenv
source .\.virtualenv\Scripts\activate
pip install -r requirements.txt
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
