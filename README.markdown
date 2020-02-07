# Rough Trade Calendar

[![CircleCI](https://img.shields.io/circleci/build/github/craiga/rough-trade-calendar.svg)](https://circleci.com/gh/craiga/rough-trade-calendar) [![Security Headers](https://img.shields.io/security-headers?url=https%3A%2F%2Frough-trade-calendars.craiga.id.au)](https://securityheaders.com/?q=https%3A%2F%2Frough-trade-calendars.craiga.id.au)

Web site and iCalendar feeds listing upcoming Rough Trade in-store events.

***In no way affiliated with Rough Trade!***

## Running Web Site Locally

```
pipenv install
printf "DEBUG=1\n" > .env
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

## GraphQL

This site has a GraphQL API at https://rough-trade-calendars.craiga.id.au/graphql. [Have a play around with it!](https://rough-trade-calendars.craiga.id.au/graphql#query=%7B%0A%20%20allLocations%20%7B%0A%20%20%20%20totalCount%0A%20%20%20%20edges%20%7B%0A%20%20%20%20%20%20node%20%7B%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%20%20events(first%3A%205%2C%20startAfter%3A%20%222019-12-31T23%3A59%3A59%2B00%3A00%22%2C%20orderBy%3A%20%22startAt%22)%20%7B%0A%20%20%20%20%20%20%20%20%20%20totalCount%0A%20%20%20%20%20%20%20%20%20%20pageInfo%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20hasNextPage%0A%20%20%20%20%20%20%20%20%20%20%20%20hasPreviousPage%0A%20%20%20%20%20%20%20%20%20%20%20%20startCursor%0A%20%20%20%20%20%20%20%20%20%20%20%20endCursor%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20edges%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20node%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20description%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20startAt%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A%0A)
