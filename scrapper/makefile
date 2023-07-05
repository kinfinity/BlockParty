NAME := ipfsscrapper
INSTALL_STAMP := .install.stamp
POETRY := $(shell command -v poetry 2> /dev/null)

export environment=$(profile)

.DEFAULT_GOAL := 

# GIT commit id will be used as version of the application
# VERSION ?= $(shell git rev-parse --short HEAD)
VERSION := 1.0.0

DOCKER_IMAGE_NAME := "$(NAME):$(VERSION)"
DOCKER_CONTAINER_NAME := "$(NAME)-$(VERSION)"

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install     install packages and prepare environment"
	@echo "  clean       remove all temporary files"
	@echo "  lint        run the code linters"
	@echo "  format      reformat code"
	@echo "  test        run all the tests"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install
	touch $(INSTALL_STAMP)

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP) .coverage .mypy_cache

.PHONY: lint
lint: $(INSTALL_STAMP)
	$(POETRY) run isort --profile=black --lines-after-imports=2 ./src/$(NAME)
	$(POETRY) run black --check ./src/$(NAME) --diff
	$(POETRY) run flake8 --ignore=W503,E501 ./src/$(NAME)
	$(POETRY) run mypy ./src/$(NAME) --ignore-missing-imports
	$(POETRY) run bandit -r ./src/$(NAME) -s B608

.PHONY: format
format: $(INSTALL_STAMP)
	$(POETRY) run isort --profile=black --lines-after-imports=2 ./src/$(NAME)
	$(POETRY) run black ./src/$(NAME)

.PHONY: test
test: $(INSTALL_STAMP)
	$(POETRY) run pytest ./src/$(NAME)/tests/ --cov-report term-missing --cov-fail-under 100 --cov ./src/$(NAME)

## docker-build: Build the scrapper image
docker-build:
	$(info ---> Building Docker Image: ${DOCKER_IMAGE_NAME}, Exposed Port: ${port})
	docker build -t ${DOCKER_IMAGE_NAME} . \
		--build-arg port=${port} \

docker-build-debug:
	$(info ---> Building Docker Image: ${DOCKER_IMAGE_NAME}, Exposed Port: ${port})
	docker build --no-cache --progress plain -t ${DOCKER_IMAGE_NAME} . \
		--build-arg port=${port} \

## docker-run: Run the scrapper as a docker container
docker-run:
	$(info ---> Running Docker Container: ${DOCKER_CONTAINER_NAME} in Environment: ${profile})
	docker run --name ${DOCKER_CONTAINER_NAME} -it \
				--env environment=${profile} \
				$(DOCKER_IMAGE_NAME)

## docker-start: Builts Docker image and runs it.
docker-start: build-docker run-docker

## docker-stop: Stops the docker container
docker-stop:
	docker stop $(DOCKER_CONTAINER_NAME)

## docker-remove: Removes the docker images and containers	
docker-remove:
	docker rm $(DOCKER_CONTAINER_NAME)
	docker rmi $(DOCKER_IMAGE_NAME)

## docker-clean: Cleans all docker resources
docker-clean: docker-clean-service-images docker-clean-build-images

## docker-clean-service-images: Stops and Removes the service images
docker-clean-service-images: docker-stop docker-remove

## docker-clean-build-images: Removes build images
docker-clean-build-images: 
	docker rmi $(docker images --filter label="builder=true")
