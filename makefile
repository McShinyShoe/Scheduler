.PHONY: run deploy clean

.venv:
	python -m venv .venv

run:
	bash run.sh

deploy:
	docker compose up -d

clean:
	docker compose down