NUMCORES = $(shell grep -c ^processor /proc/cpuinfo)

all: input gen

input:
	find "$$(cd ../../gpu/single; pwd)" -name "arg.ini" | sort > arg
	find "$$(cd ../../../../build/apps/; pwd)" -name "*.so" | grep "m2s" | sort > exe
	find "$$(cd ../../../../kernel/amd/src/single/; pwd)" -name "*.cl" | sort > src
	find "$$(cd ../../../../kernel/amd/bin/single/; pwd)" -name "*.bin" | sort > bin

gen:
	python gen.py --arg arg --exe exe --src src --bin bin
	find . -mindepth 1 -maxdepth 1 -type d -exec ln -s $(PWD)/Makefile.tpl {}/Makefile \;

run:
	find . -mindepth 1 -type d -print0 | xargs -0 -P$(NUMCORES) -n1 make -C 

see:
	find . -mindepth 1 -type d -exec make -C {} see \;

tidy:
	find . -mindepth 1 -type d -exec make -C {} clean \;

purge:
	rm -f arg exe src bin *.pyc
	find . -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} \;

clean:
	rm -f arg exe src bin *.pyc
