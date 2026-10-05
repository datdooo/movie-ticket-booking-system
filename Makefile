.PHONY: install run test lint format seed docker-up docker-down load-test

install:
	python -m pip install -r requirements-dev.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff check .

format:
	ruff format .
	ruff check --fix .

seed:
	python -m scripts.seed

docker-up:
	docker compose up --build

docker-down:
	docker compose down

load-test:
	bash scripts/run_kaggle_load_test.sh
