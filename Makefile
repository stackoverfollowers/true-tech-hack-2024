PROJECT_NAME = tth
TEST_PATH = ./tests/
PYTHON_VERSION = 3.11

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

lint-ci: ruff mypy  ##@Linting Run all linters in CI


ruff: ##@Linting Run ruff
	.venv/bin/ruff check ./$(PROJECT_NAME)

mypy: ##@Linting Run mypy
	.venv/bin/mypy --config-file ./pyproject.toml ./$(PROJECT_NAME)

test: ##@Test Run tests with pytest
	pytest -vvx $(TEST_PATH)

test-ci: ##@Test Run tests with pytest and coverage in CI
	.venv/bin/coverage run -m pytest $(TEST_PATH) --junitxml=junit_report.xml
	.venv/bin/coverage report
	.venv/bin/coverage xml

develop: clean_dev ##@Develop Create virtualenv
	python$(PYTHON_VERSION) -m venv .venv
	.venv/bin/pip install -U pip poetry
	.venv/bin/poetry config virtualenvs.create false
	.venv/bin/poetry install

local: ##@Develop Run dev containers for test
	docker compose -f docker-compose.dev.yaml up --force-recreate --renew-anon-volumes --build

local_down: ##@Develop Stop dev containers with delete volumes
	docker compose -f docker-compose.dev.yaml down -v

alembic-upgrade-head: ##@Database Run alembic upgrade head
	.venv/bin/python -m $(PROJECT_NAME).db --pg-dsn=$(APP_DB_PG_DSN) upgrade head

alembic-downgrade:  ##@Database Run alembic downgrade to previous version
	.venv/bin/python -m $(PROJECT_NAME).db --pg-dsn=$(APP_DB_PG_DSN) downgrade -1

alembic-revision:  ##@Database New alembic revision
	.venv/bin/python -m $(PROJECT_NAME).db --pg-dsn=$(APP_DB_PG_DSN) revision --autogenerate

docker-alembic-upgrade-head: ##@Database Run alembic upgrade head in docker
	docker-compose exec backend python -m $(PROJECT_NAME).db upgrade head

clean_dev:  ##@Develop Remove virtualenv
	rm -rf .venv

cloc: ##@Help Run cloc
	cloc --exclude-dir=$(shell tr '\n' ',' < .clocignore) .