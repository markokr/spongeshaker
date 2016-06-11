
PYTHON = python
PYVER := $(shell $(PYTHON) -c 'import sys;print("%d.%d"%sys.version_info[:2])')
BUILD_DIR := build/lib.$(PYVER)
BUILD_OPTS = --build-lib=$(BUILD_DIR)

all:
	tox

docs:
	tox -e docs

clean:
	rm -rf build */*.pyc doc/_build spongeshaker/__pycache__

tags:
	ctags src/*.[ch]

deb:
	debuild -us -uc -b

debclean: clean
	rm -rf debian/python* debian/files debian/tmp

upload:
	python setup.py sdist upload

.PHONY: tags deb clean docs debclean upload all

