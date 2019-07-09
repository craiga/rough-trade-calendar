release: python manage.py migrate --no-input && python manage.py loaddata locations && scrapy crawl rough_trade_events
web: python manage.py check --deploy --fail-level WARNING && gunicorn rough_trade_calendar.wsgi --log-file -
