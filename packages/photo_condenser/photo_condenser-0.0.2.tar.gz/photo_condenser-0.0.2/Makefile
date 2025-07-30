.PHONY: clean test docs build release_local release_remote install build_venv

clean:
	rm -rf build/ dist/ .eggs/
	find . -name '__pycache__' -exec rm -r {} +
	rm -rf .coverage htmlcov

test:
	pytest

docs:
	$(MAKE) -C docs html

build: clean
	venv/bin/flit build

release_local: clean test build
	venv/bin/flit publish


release_remote:
	venv/bin/bump2version patch
	git push
	git push --tags

install:
	venv/bin/flit install --editable


build_venv:
	python -m venv venv
	venv/bin/pip install .[dev]
	venv/bin/pre-commit install
