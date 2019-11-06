# Rough Trade Calendar

![CircleCI](https://img.shields.io/circleci/build/github/craiga/rough-trade-calendar.svg) ![Security Headers](https://img.shields.io/security-headers?url=https%3A%2F%2Frough-trade-calendar.herokuapp.com)

Web site and iCalendar feeds listing upcoming Rough Trade in-store events.

***In no way affiliated with Rough Trade!***

## Running Web Site Locally

```
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py loaddata locations
pipenv run python manage.py runserver
```

## Running Tests and Code Quality Tools

```
pipenv install --dev
pipenv run isort --check-only
pipenv run black --check --diff .
find . -iname "*.py" | xargs pipenv run pylint
pipenv run pytest
```

## Scraping Web Sites for Events

```
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py loaddata locations
pipenv run scrapy crawl rough_trade_events
pipenv run scrapy crawl rough_trade_event_detail
```
