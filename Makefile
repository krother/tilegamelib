.PHONY: tests coverage devinstall

help:
	@echo "tests - run tests"
	@echo "coverage - run tests with coverage enabled"
	@echo "devinstall - install packages required for development"
	@echo "release - release on pypi"

tests:
	py.test ${OPTS}

coverage:
	py.test ${OPTS} --cov

devinstall:
	pip install -e .
	pip install -e .[tests]

lint:
	coala --ci

release:
	pip install twine
	python setup.py sdist
	twine upload dist/*
