all: input gen

input:
	find "$$(cd ../../../../build64/apps/; pwd)" -name "*.so" | grep -v "m2s" | sort > exe
	find "$$(cd ../../../../kernel/amd/src/single/; pwd)" -name "*.cl" | sort > src
	find "$$(cd ../../../../kernel/amd/src/fusion; pwd)" -name "*.cl" | sort > mrg

gen:
	python gen.py --cu 44 --exe exe --src src --mrg mrg
	rm -f exe src mrg *.pyc
	find . -mindepth 1 -type d -exec ln -s $(PWD)/Makefile.tpl {}/Makefile \;

perf:
	find . -mindepth 1 -type d -exec make -C {} perf \;

see:
	find . -mindepth 1 -type d -exec make -C {} see \;

diff:
	find . -mindepth 1 -type d -exec make -C {} diff \;

verify:
	find . -name "diff" ! -size 0 | sort -n > wrong
	find . -name "diff" -size 0 | sort -n > right

speedup: verify
	rm -f speedup*
	echo 'benchmark, speedup' > speedup
	echo 'benchmark, speedup' > speedup_r
	echo 'benchmark, speedup' > speedup_w
	sed 's/diff/log/g' right | xargs -I % sh -c 'find % -exec grep "Speedup" {} /dev/null \; ' | awk -F'[/=]' '{print $$2 "," $$4}' >> speedup_r
	sed 's/diff/log/g' wrong | xargs -I % sh -c 'find % -exec grep "Speedup" {} /dev/null \; ' | awk -F'[/=]' '{print $$2 "," $$4}' >> speedup_w
	find ./ -name "log" -exec grep "Speedup" {} /dev/null \; | awk -F'[/=]' '{print $$2 "," $$4}' >> speedup

clean:
	find . -mindepth 1 -type d -exec make -C {} clean \;

purge:
	rm -f exe src mrg *.pyc wrong right
	find -mindepth 1 -type d -prune -exec rm -r {} \;
