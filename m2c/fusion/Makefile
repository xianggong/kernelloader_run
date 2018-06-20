NUMCORES = $(shell grep -c ^processor /proc/cpuinfo)

all: input gen

input:
	find "$$(cd ../../amd/gpu/single; pwd)" -name "arg.ini" | sort > arg
	find "$$(cd ../../../build/apps/; pwd)" -name "*.so" | grep "m2s" | sort > exe
	find "$$(cd ../../../kernel/m2c/src/single/; pwd)" -name "*.cl" | sort > src
	find "$$(cd ../../../kernel/m2c/bin/single/; pwd)" -name "*.bin" | sort > bin
	find "$$(cd ../../../kernel/m2c/src/fusion; pwd)" -name "*.cl" | sort > msrc
	find "$$(cd ../../../kernel/m2c/bin/fusion; pwd)" -name "*.bin" | sort > mbin
	cp ../../../result/gpu ./mflt

gen: input
	python gen.py --arg arg --exe exe --src src --bin bin --msrc msrc --mbin mbin --mflt mflt
	find . -mindepth 1 -maxdepth 1 -type d -exec ln -s $(PWD)/Makefile.1.tpl {}/Makefile \;
	find . -mindepth 2 -type d -exec ln -s $(PWD)/Makefile.tpl {}/Makefile \;
	rm -f arg exe *src *bin *mflt *.pyc

run:
	find . -mindepth 2 -type d -print0 | xargs -0 -P$(NUMCORES) -n1 make -C 

tidy:
	find . -mindepth 1 -type d -exec make -C {} clean \;

purge:
	rm -f arg exe *src *bin *mflt *.pyc
	find . -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} \;

clean:
	rm -f arg exe src bin *.pyc
	find . -mindepth 1 -maxdepth 1 -type d -exec make -C {} clean \;
