test:
	echo "TDD tests:"
	python3 -m unittest unittests.py
	echo "BDD tests:"
	behave
run:
	python3 main.py
build:
	bash build.sh
