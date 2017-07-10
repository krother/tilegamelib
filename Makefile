.PHONY: tests coverage devinstall

help:
	@echo "tests - run tests"
	@echo "coverage - run tests with coverage enabled"
	@echo "devinstall - install packages required for development"

tests:
	py.test ${OPTS}

coverage:
	py.test ${OPTS} --cov

devinstall:
	pip install -e .
	pip install -e .[tests]

lint:
	coala --ci
