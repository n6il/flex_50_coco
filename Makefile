all:
	make -C OS all
	make -C APPS all

clean:
	make -C OS clean
	make -C APPS clean

