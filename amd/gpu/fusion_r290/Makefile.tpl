all: perf 

verify: clean
	find -name "*.ini" -exec bash -c "../../../../../build64/loader/src/loader --logtostderr=1 --repeat=1 --config={} > log 2>&1" \;
	find -name "output*" -printf "%f\n" | xargs -I % sh -c 'find ../../single -name % -exec diff ./% {} \;' > diff 2>&1

perf: verify
	test ! -s diff && find -name "*.ini" -exec bash -c "../../../../../build64/loader/src/loader --logtostderr=1 --config={} > log 2>&1" \;
	rm -rf *input* *output* 

seeperf: verify
	test ! -s diff && find -name "*.ini" -exec ../../../../../build64/loader/src/loader --logtostderr=1 --config={} \;

diff:
	find -name "output*" -printf "%f\n" | xargs -I % sh -c 'find ../../single -name % -exec diff ./% {} \;' > diff 2>&1

catdiff:
	test -f diff  && cat diff

clean:
	rm -rf *input* *output* *log* *INFO* *ERROR* *diff*
