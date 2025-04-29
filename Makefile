build:
	@docker build -t test-image --target development .

test: build
	@docker run --rm \
        --name test-container \
        -e PYTHONPATH=/code \
        -v $(shell pwd):/code \
    test-image pytest -vvv


lint: build
	docker run --rm -t \
		--name test-container \
        -e PYTHONPATH=/code \
		-v $(shell pwd):/code \
		test-image \
		sh -c "ruff check src"

shell: build
	docker run --rm -it \
		--name debug-container \
		-e PYTHONPATH=/code \
		-v $(shell pwd):/code \
		test-image \
		bash

run:
	docker run --rm -it \
		--name app-container \
		-p 8080:8080 \
		-e PYTHONPATH=/code \
		-v $(shell pwd):/code \
		test-image \
		uvicorn src.main:app --host 0.0.0.0 --port 8080 --app-dir src