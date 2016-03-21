# Makefile ruedaerueda

DJADMIN_PY=$(VIRTUAL_ENV)/bin/django-admin.py
FABRIC=$(VIRTUAL_ENV)/bin/fab
GUNICORN=$(VIRTUAL_ENV)/bin/gunicorn
MANAGE_PY=$(VIRTUAL_ENV)/bin/python manage.py
PIP=$(VIRTUAL_ENV)/bin/pip
PROVY=$(VIRTUAL_ENV)/bin/provy
PY=$(VIRTUAL_ENV)/bin/python
UWSGI=$(VIRTUAL_ENV)/bin/uwsgi

SETTINGS_DEV=ruedaerueda.settings.dev
SETTINGS_PROD=ruedaerueda.settings.prod
SETTINGS_STAGE=ruedaerueda.settings.stage
SETTINGS_TEST=ruedaerueda.settings.test

# These targets are not files
.PHONY: all dev prod stage test boot reboot requirements createsuperuser shell clean clean.migrations pep8 compile help runserver server gunicorn uwsgi translate.br makemessages compilemessages db db.delete.sqlite3 db.reboot db.clear mig makemig fixtures.initial static tests coverage heroku.remote heroku.create heroku.delete heroku.static heroku.migrate heroku.push heroku.deploy heroku.db.reset open vm check.venv check.app check.file check.settings check.user check.email check.branch spiders.kill spiders.seglider spiders.seglider_processos_hoje crawler.upload crawler.seglider.hoje crawler.seglider.todos

all: help

check.venv:
	@if test "$(VIRTUAL_ENV)" = "" ; then echo "VIRTUAL_ENV is undefined"; exit 1; fi

check.app:
	@if test "$(APP)" = "" ; then echo "APP is undefined"; exit 1; fi

check.file:
	@if test "$(FILE)" = "" ; then echo "FILE is undefined"; exit 1; fi

check.settings:
	@if test "$(SETTINGS)" = "" ; then echo "SETTINGS is undefined"; exit 1; fi

check.branch:
	@if test "$(BRANCH)" = "" ; then echo "BRANCH is undefined"; exit 1; fi

check.user:
	@if test "$(USER)" = "" ; then echo "USER is undefined"; exit 1; fi

check.email:
	@if test "$(EMAIL)" = "" ; then echo "EMAIL is undefined"; exit 1; fi

# SETTINGS FILES

dev: check.venv
	$(eval SETTINGS:=$(SETTINGS_DEV))

prod: check.venv
	$(eval SETTINGS:=$(SETTINGS_PROD))

stage: check.venv
	$(eval SETTINGS:=$(SETTINGS_STAGE))

test: check.venv
	$(eval SETTINGS:=$(SETTINGS_TEST))

# ---

# UTIL

requirements:
	@$(PIP) install -r requirements.txt

createsuperuser: check.user check.email check.settings
	@echo "Creating SUPERUSER:"
	@$(MANAGE_PY) createsuperuser --username=$(USER) --email=$(EMAIL) --settings=$(SETTINGS)

shell: check.settings
	@$(MANAGE_PY) shell --settings=$(SETTINGS)

clean:
	@find . -name '*.pyc' -exec rm -f {} \;
	@find . -name 'Thumbs.db' -exec rm -f {} \;
	@find . -name '*~' -exec rm -f {} \;

clean.scrapyd:
	@rm -rf build
	@rm -rf *.egg-info
	@rm -rf scrapyd_build

clean.migrations:
	@git ls-files | grep migrations > skip_migrations
	@find ruedaerueda -path "*/apps/site_modules/*" | grep migrations >> skip_migrations
	@echo 'Migrações a serem removidas:'
	@find . -path "*/migrations/*.py*" | grep -vFf skip_migrations
	@find . -path "*/migrations/*.py*" | grep -vFf skip_migrations | xargs rm
	@echo 'Migrações removidas com sucesso!'
	@rm skip_migrations

pep8:
	@pep8 --filename="*.py" --ignore=W --exclude="manage.py,settings.py,migrations" --first --show-source --statistics --count ruedaerueda

compile:
	@$(PY) -m compileall ruedaerueda

help:
	@echo 'Just a makefile to help django-projects.'

boot: db createsuperuser

reboot: db.fresh createsuperuser

# ---

# SERVER

runserver: check.settings
	@$(MANAGE_PY) runserver --settings=$(SETTINGS)

server: check.settings
	@$(MANAGE_PY) runserver 0.0.0.0:8000 --settings=$(SETTINGS)

gunicorn: check.settings
	@$(GUNICORN) ruedaerueda.wsgi -w 4 -b 127.0.0.1:8000 --settings=$(SETTINGS)

# ---

# DATABASE

db: check.settings makemig mig fixtures.initial

db.delete.sqlite3:
	@rm ruedaerueda/db/ruedaerueda.sqlite3

db.reboot: db.delete.sqlite3 db

db.clear: check.app check.settings
	@$(MANAGE_PY) sqlclear $(APP) --settings=$(SETTINGS) | $(MANAGE_PY) dbshell --settings=$(SETTINGS)

mig: check.settings
	@$(MANAGE_PY) migrate --settings=$(SETTINGS)

makemig: check.settings
	@$(MANAGE_PY) makemigrations --settings=$(SETTINGS)

fixtures.initial: check.settings
	@$(MANAGE_PY) loaddata ruedaerueda/db/fixtures/01-groups.json --settings=$(SETTINGS)
	@$(MANAGE_PY) loaddata ruedaerueda/db/fixtures/02-accounts.json --settings=$(SETTINGS)
	@$(MANAGE_PY) loaddata ruedaerueda/db/fixtures/03-comarcas.json --settings=$(SETTINGS)
	@$(MANAGE_PY) loaddata ruedaerueda/db/fixtures/04-correspondentes.json --settings=$(SETTINGS)

# ---

# STATIC

static: check.settings
	@$(MANAGE_PY) collectstatic --clear --noinput --settings=$(SETTINGS)

# ---

# CRAWLERS

crawler.upload:
	@scrapyd-deploy staging -p crawlers

crawler.seglider.hoje:
	@curl http://staging.ruedaerueda.adv.br:6800/schedule.json -d project=crawlers -d spider=seglider_processos_hoje

crawler.seglider.todos:
	@curl http://staging.ruedaerueda.adv.br:6800/schedule.json -d project=crawlers -d spider=seglider_processos_todos

crawler.cancel:
	@curl http://staging.ruedaerueda.adv.br:6800/cancel.json -d project=crawlers -d job=$(JOB)

# ---

# SPIDERS

spiders.kill:
	@ps aux | grep "scrapy crawl" | grep -v grep | awk "{ print \$2 }" | xargs kill -9

spiders.seglider:
	scrapy crawl seglider -o processos.json -t json -s JOBDIR=jobdir

spiders.seglider_processos_hoje:
	scrapy crawl seglider_processos_hoje -o seglider_processos_hoje.json -t json -s JOBDIR=jobdir

# ---

# TESTS

tests:
	@$(MANAGE_PY) test --settings=$(SETTINGS_TEST)

coverage:
	@$(MANAGE_PY) test_coverage --settings=$(SETTINGS_TEST)


# CELERY


# RABBITMQ

celery: check.settings
	@$(MANAGE_PY) celery worker --loglevel=INFO --settings=$(SETTINGS)

celery.beat: check.settings
	@$(MANAGE_PY) celery beat --settings=$(SETTINGS)

celery.purgeall: check.settings
	@$(MANAGE_PY) celery purge --settings=$(SETTINGS)
