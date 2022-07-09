.PHONY: tests coverage devinstall

help:
	@echo "tests - run tests"
	@echo "coverage - run tests with coverage enabled"
	@echo "devinstall - install packages required for development"
	@echo "release - release on pypi"

tests:
	pytest ${OPTS}

coverage:
	pytest ${OPTS} --cov

devinstall:
	pip install -e .
	pip install -e .[tests]

release:
	pip install twine
	python setup.py sdist
	twine upload dist/*
