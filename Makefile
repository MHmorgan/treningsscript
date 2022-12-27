CONF=src/.clasp.JSON

all: watch

push: $(CONF)
	cd src && clasp push

watch: $(CONF)
	cd src && clasp push -w

status: $(CONF)
	cd src && clasp status

$(CONF):
	echo '{"scriptId":"<script-id>", "rootDir":"${PWD}/src"}' > src/.clasp.json

