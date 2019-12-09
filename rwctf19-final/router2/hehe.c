#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

int main(int argc, char **argv) {
    printf("hehehe\n");
    const char *path = argc > 1 ? argv[1] : "/tmp/haha";
    unlink(path);
    int s = socket(AF_UNIX, SOCK_DGRAM, 0);
    printf("fd = %d\n", s);
    struct sockaddr_un addr;
    addr.sun_family = AF_UNIX;
    strcpy(addr.sun_path, path);
    if (bind(s, (struct sockaddr *)&addr, sizeof(struct sockaddr_un)) == -1) {
        perror("bind");
        return 1;
    }
    char buf[1024];
    while (1) {
        struct sockaddr_un client = {0};
        int sz = sizeof(client);
        int l = recvfrom(s, &buf, sizeof(buf) - 1, 0, (struct sockaddr *)&client, &sz);
        if (l == -1) {
            perror("recvfrom");
        } else {
            buf[l] = 0;
            printf("received %d: %s\n", l, buf);
            const char *reply = NULL;
            const char *req = NULL;
            if (!memcmp(buf, "ATTACH", 6)) {
                reply = "OK\n";
                // req = "CTRL-EVENT-TERMINATING ";
                req = "AP-ENABLED ";
            } else if (!memcmp(buf, "PING", 4)) {
                reply = "PONG";
            } else if (!memcmp(buf, "DETACH", 6)) {
                reply = "OK\n";
            }
            if (reply != NULL && sendto(s, reply, strlen(reply), 0, (struct sockaddr *)&client, sz) == -1) {
                perror("sendto/reply");
            }
            if (req != NULL && sendto(s, req, strlen(req), 0, (struct sockaddr *)&client, sz) == -1) {
                perror("sendto/req");
            }
        }
    }
    return 0;
}
