
PYTHON = python
PYVER := $(shell $(PYTHON) -c 'import sys;print("%d.%d"%sys.version_info[:2])')
BUILD_DIR := build/lib.$(PYVER)
BUILD_OPTS = --build-lib=$(BUILD_DIR)

vlist = 2.6 2.7 3.1 3.2 3.3 3.4

all:
	$(PYTHON) setup.py build -q $(BUILD_OPTS)
	cd $(BUILD_DIR) && $(PYTHON) -m spongeshaker.test

full: clean
	@for v in $(vlist); do \
	  echo "Testing: python$$v"; \
	  make -s PYTHON=python$$v || exit 1; \
	done

doc2:
	cd $(BUILD_DIR) && pydoc spongeshaker

doc3:
	make doc2 PYTHON=python3

clean:
	rm -rf build */*.pyc doc/_build

tags:
	ctags src/*.[ch]

deb:
	debuild -us -uc -b

debclean: clean
	rm -rf debian/python-spongeshaker* debian/files

.PHONY: tags deb clean doc2 doc3

