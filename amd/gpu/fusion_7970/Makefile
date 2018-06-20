all: input gen

input:
	find "$$(cd ../../gpu/single; pwd)" -name "arg.ini" | sort > arg
	find "$$(cd ../../../../build/apps/; pwd)" -name "*.so" | grep -v "m2s" | sort > exe
	find "$$(cd ../../../../kernel/amd/src/single/; pwd)" -name "*.cl" | sort > src
	find "$$(cd ../../../../kernel/amd/src/fusion; pwd)" -name "*.cl" | sort > mrg

gen:
	python gen.py --cu 32 --arg arg --exe exe --src src --mrg mrg
	rm -f exe src mrg *.pyc
	find . -mindepth 1 -type d -exec ln -s $(PWD)/Makefile.tpl {}/Makefile \;

run:
	find . -mindepth 1 -type d -exec make -C {} run \;

runv:
	find . -mindepth 1 -type d -exec make -C {} verify \;

see:
	find . -mindepth 1 -type d -exec make -C {} see \;

diff:
	find . -mindepth 1 -type d -exec make -C {} diff \;

verify:
	find . -name "diff" ! -size 0 | sort -n > wrong
	find . -name "diff" -size 0 | sort -n > right
	sed -i "s/diff//g" wrong
	sed -i "s/diff//g" right 

speedup: 
	rm -f *speedup*
	find ./ -name "log" -exec grep "Speedup" {} /dev/null \; | awk -F'[/=]' '{print $$2 "," $$4}' >> speeduptmp
	sort -V speeduptmp > speedup
	rm -f speeduptmp
	sed -i '1s/^/benchmark, speedup\n/' speedup

clean:
	find . -mindepth 1 -type d -exec make -C {} clean \;

purge:
	rm -f exe src mrg *.pyc wrong right
	rm -rf `find . -mindepth 1 -type d`
