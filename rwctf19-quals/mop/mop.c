#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/fcntl.h>
#include <sys/time.h>
#include <sys/resource.h>

int main(int argc, char **argv) {
	char buf[0x100];
	int rp[2], wp[2];
	pipe(&rp);
	pipe(&wp);
	int pid = fork();
	if (!pid) {
		dup2(wp[1], 1);
		dup2(rp[0], 0);
		close(wp[0]);
		close(rp[1]);
		execl("/readflag", "readflag", NULL);
	} else {
		dup2(wp[0], 0);
		close(rp[0]);
		close(wp[1]);
		char buf[0x100];
		gets(&buf);
		puts(buf);
		int a, b, c, d, e;
		char w, x, y, z;
		scanf("(((((%lld)%c(%lld))%c(%lld))%c(%lld))%c(%lld))", &a, &w, &b, &x, &c, &y, &d, &z, &e);
		if (w == '+') {
			a += b;
		} else {
			a -= b;
		}
		if (x == '+') {
			a += c;
		} else {
			a -= c;
		}
		if (y == '+') {
			a += d;
		} else {
			a -= d;
		}
		if (z == '+') {
			a += e;
		} else {
			a -= e;
		}
		// printf("%lld %lld %lld %lld %lld", a, b, c, d, e);
		dprintf(rp[1], "%d\n", a);
		while (gets(&buf) != NULL) {
			puts(buf);
		}
	}
}
