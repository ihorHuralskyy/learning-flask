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
