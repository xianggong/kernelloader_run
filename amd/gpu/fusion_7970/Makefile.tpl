all: run

run:
	test ! -f log && find -name "*.ini" -exec bash -c "../../../../../build/loader/src/loader --logtostderr=1 --config={} > log 2>&1" \;
	find -name "output*" -exec rm -f {} \;
	find -name "input*" -exec rm -f {} \;

runverify:
	test ! -f log && find -name "*.ini" -exec bash -c "../../../../../build/loader/src/loader --logtostderr=1 --repeat=1 --config={} > log 2>&1" \;

verify:
	test ! -f log && find -name "*.ini" -exec bash -c "../../../../../build/loader/src/loader --logtostderr=1 --repeat=1 --config={} > log 2>&1" \;
	find -name "output*" -printf "%f\n" | xargs -I % sh -c 'find ../../single -name % -exec diff ./% {} \;' > diff 2>&1
	find -name "output*" -exec rm -f {} \;
	find -name "input*" -exec rm -f {} \;

see:
	test ! -f log && find -name "*.ini" -exec ../../../../../build/loader/src/loader --logtostderr=1 --config={} \;

diff:
	find -name "output*" -printf "%f\n" | xargs -I % sh -c 'find ../../single -name % -exec diff ./% {} \;' > diff 2>&1

catdiff:
	test -f diff && cat diff

clean:
	rm -rf *input* *output* *log* *INFO* *ERROR* diff
