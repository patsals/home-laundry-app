run:
	cd api_server && \
	uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload

env:
	cd api_server && \
	uv venv --clear && \
	uv sync