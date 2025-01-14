.PHONY: initdb run psqlcli

initdb:
	@echo ">>> Initializing database..."
	python3 -m app.scripts.init_db

run:
	@echo ">>> Starting fastapi server..."
	fastapi dev app/main.py --port 8080

psqlcli:
	@echo ">>> Entering PostgreSQL cli..."
	psql -U myuser -d paypal_test