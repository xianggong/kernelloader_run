all:

run:
	find . -mindepth 1 -type d -exec make -C {} run \;
	
clean:
	find . -mindepth 1 -type d -exec make -C {} clean \;
