CONF=src/.clasp.JSON

all: build

build:
	elm make --optimize elm/Main.elm --output=src/index.html

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
