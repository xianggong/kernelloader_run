all:

run:
	find . -mindepth 1 -type d -exec make -C {} run \;

see:
	find . -mindepth 1 -type d -exec make -C {} see \;
	
clean:
	find . -mindepth 1 -type d -exec make -C {} clean \;
