
IMG=treningserver

all: build

docker:
	docker run --rm -p 8000:8000 $(IMG)

flask:
	flask --debug run

run:
	gunicorn -w 4 'app:create_app()'

build:
	docker build -t $(IMG) app

