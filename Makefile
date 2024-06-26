# Run python api server.
# uvicorn main:app  --reload --host 0.0.0.0 --port 8000
# Usage: make run
run:
	poetry run uvicorn gutenberg.api:app --reload


# Start elasticsearch in Docker.
# Usage: make start_es
start_es:
	./start_es.sh
