# Create a makefile command to run a fastapi server with uvicorn
# Usage: make run
run:
	poetry run uvicorn gutenberg.api:app --reload
