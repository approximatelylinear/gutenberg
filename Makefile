# Run python api server.
# Usage: make run
run:
	poetry run uvicorn gutenberg.api:app --reload

# Start elasticsearch in Docker.
# Usage: make start_es
start_es:
	./start_es.sh
