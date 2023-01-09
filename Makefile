CONF=src/.clasp.JSON

JS=elm.js
MIN=elm.min.js
OUT=src/index.html
START=index.start.html
END=index.end.html

all: build

# npm install uglify-js -g
build:
	elm make --optimize elm/Main.elm --output=$(JS)
	uglifyjs $(JS) --compress 'pure_funcs=[F2,F3,F4,F5,F6,F7,F8,F9,A2,A3,A4,A5,A6,A7,A8,A9],pure_getters,keep_fargs=false,unsafe_comps,unsafe' | uglifyjs --mangle --output $(MIN)
	cat $(START) $(MIN) $(END) > $(OUT)


pull: $(CONF)
	cd src && clasp pull

push: $(CONF)
	cd src && clasp push

watch: $(CONF)
	cd src && clasp push -w

status: $(CONF)
	cd src && clasp status

$(CONF):
	echo '{"scriptId":"1EcmC727o3JoS-snKx-16wJnK-q4ZlAWHraqd2Hc7CFyz1c6ja_gO4a5I", "rootDir":"${PWD}/src"}' > src/.clasp.json
