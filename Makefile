VENV_NAME=venv

venv:
	test -d $(VENV_NAME) || virtualenv $(VENV_NAME) -p python3
	. $(VENV_NAME)/bin/activate
	pip install -r requirements.txt

run:
	docker-compose up

stop:
	docker-compose down

format: venv
	black .

clean:
	rm -rf $(VENV_NAME)


venvV: env/bin/activate
env/bin/activate: requirements.txt
	test -d env || python3 -m venv env
	env/bin/pip install --upgrade pip pip-tools
	env/bin/pip install -Ur requirements.txt
	touch env/bin/activate
