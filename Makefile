
flask:
	flask --debug run -p 8000

run:
	gunicorn -w 4 'app:create_app()'


# Docker

NAME=trapp
ARGS=--rm -p 8000:8000 -v $(shell pwd):/data

build:
	docker build --tag $(NAME):dev .

docker:
	docker run $(ARGS) $(NAME):dev
