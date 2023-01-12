
JS=app/static/elm.js
MIN=app/static/elm.min.js

IMG=treningserver

all: build

docker:
	docker run --rm -p 8000:8000 $(IMG)

flask:
	flask --debug run

run:
	gunicorn -w 4 'app:create_app()'

build: build-elm build-docker

# npm install uglify-js -g
build-elm:
	elm make --optimize elm/Main.elm --output=$(JS)
	uglifyjs $(JS) --compress 'pure_funcs=[F2,F3,F4,F5,F6,F7,F8,F9,A2,A3,A4,A5,A6,A7,A8,A9],pure_getters,keep_fargs=false,unsafe_comps,unsafe' | uglifyjs --mangle --output $(MIN)

build-docker:
	docker build -t $(IMG) app
