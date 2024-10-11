test:
	echo "TDD tests:"
	python3 -m unittest unittests.py
	echo "BDD tests:"
	behave
run:
	python3 main.py
build:
	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt
