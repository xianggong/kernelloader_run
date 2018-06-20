SUBDIRS = $(shell ls -d */)

all: input gen

input:
	find "$$(cd ../../../../build64/apps/; pwd)" -name "*.so" | sort > exe
	find "$$(cd ../../../../kernel/amd/src/single/; pwd)" -name "*.cl" | sort > src
	find "$$(cd ../../../../kernel/amd/bin/single/; pwd)" -name "*.bin" | sort > bin

gen:
	python gen.py --exe exe --src src --bin bin
	rm -f exe src bin *.pyc
	find . -mindepth 1 -type d -exec ln -s ${PWD}/Makefile.tpl {}/Makefile \;

upMakeFile:
	find . -mindepth 1 -type d -exec ln -s ${PWD}/Makefile.tpl {}/Makefile \;

run:
	find . -mindepth 1 -type d -exec make -C {} run \;

once:
	find . -mindepth 1 -type d -exec make -C {} once \;

see:
	find . -mindepth 1 -type d -exec make -C {} see \;

tidy:
	find . -mindepth 1 -type d -exec make -C {} clean \;

clean:
	rm -f exe src bin *.pyc

purge:
	rm -f exe src bin *.pyc
	rm -rf `find . -mindepth 1 -type d`

