all: run

once:
	test ! -f log && find -name "*.ini" -exec bash -c "../../../../../build64/loader/src/loader --repeat=1 --logtostderr=1 --config={} > log 2>&1 " \;
	echo "i\n1" > arg.ini
	find `pwd` -name "*input*" | sort >> arg.ini

run:
	test ! -f log && find -name "*.ini" -exec bash -c "../../../../../build64/loader/src/loader --logtostderr=1 --config={} > log 2>&1 " \;
	echo "i\n1" > arg.ini
	find `pwd` -name "*input*" | sort >> arg.ini

see:
	test ! -f log && find -name "*.ini" -exec ../../../../../build64/loader/src/loader --logtostderr=1 --config={} \;
	echo "i\n1" > arg.ini
	find `pwd` -name "*input*" | sort >> arg.ini

clean:
	rm -rf *input* *log* *output* *arg*
