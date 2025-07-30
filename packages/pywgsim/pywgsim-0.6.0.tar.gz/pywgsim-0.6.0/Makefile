
UNAME := $(shell uname -s)
SNAME := pywgsim/lib/wgsim_mod.c
PNAME := scripts/pywgsim-$(UNAME)
CFLAGS := -g -O2 -Wall

.PHONY: build clean sdist devel

all:
	@echo "Compiling $(PNAME)"
	gcc $(CFLAGS) -o $(PNAME) $(SNAME) -lz -lm

clean:
	rm -rf dist build pywgsim.egg-info scripts/pywgsim-*

test:
	python -m pywgsim --help
	mkdir -p test/tmp
	(cd test && pywgsim lambda.fa tmp/read1.fq tmp/read2.fq -g tmp/output.gff)
	cat test/tmp/output.gff | head


sdist:
	python setup.py sdist

devel:
	python setup.py develop

build:
	python setup.py sdist

upload: build
	rm -rf dist
	python setup.py sdist
	#python -m twine upload --repository testpypi dist/*
	python -m twine upload --repository pypi dist/*

.PHONY: test	