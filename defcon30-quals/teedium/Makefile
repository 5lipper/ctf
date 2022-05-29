all: x

payload.h: x.py
	python3 x.py

x: x.c payload.h Makefile
	arm-linux-gnueabi-gcc -Wl,-I/lib/ld-linux-armhf.so.3 -pie -Os -o x x.c libteec.so libc-2.31.so ld-linux-armhf.so.3
	arm-linux-gnueabi-strip x
	gzip -c x | xxd -p > xx
