.PHONY: start
start:
	@docker compose --profile dagster build
	@docker compose --profile dagster up

.PHONY: start-detached
start-detached:
	@docker compose --profile dagster build
	@docker compose --profile dagster up -d

.PHONY: restart-data-analytics
restart-data-analytics:
	@docker container restart $(docker ps -aqf "name=data-analytics")

.PHONY: restart-data-science
restart-data-science:
	@docker container restart $(docker ps -aqf "name=data-science")

.PHONY: down
down:
	@docker compose --profile dagster down --remove-orphans

.PHONY: fmt
fmt:
	@docker compose build -- format
	@docker compose run -- format

.PHONY: test-data-analytics
test-data-analytics:
	@docker compose build -- data-analytics-test
	@docker compose run -- data-analytics-test

.PHONY: test-data-science
test-data-science:
	@docker compose build -- data-science-test
	@docker compose run -- data-science-test