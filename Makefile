### Total app
run: build
	docker-compose up -d

build:
	docker-compose build

stop: 
	docker-compose down

logs:
	docker-compose logs db

# DANGEROUS - WILL RESULT IN DATA LOSS
clean:
	docker-compose down || echo "..."
	docker volume rm home-laundry-app_postgres_data
	docker volume rm home-laundry-app_grafana_data


### API Server
api-server-run-docker:
	cd api_server && \
	docker build -t laundry-api-server . && \
	docker run -it --rm \
		-p 8000:8000 \
		-v $$(pwd):/app \
		laundry-api-server \
		python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload

api-server-run:
	cd api_server && \
	uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload

api-server-env:
	cd api_server && \
	uv venv --clear && \
	uv sync


### Database
# while in terminal type "\q" to quit
db-connect: stop run
	docker-compose exec db psql -U user -d laundry 
