up:
	docker compose down
	docker compose build
	docker compose up
prune:
	docker container prune -f
	docker image prune -f