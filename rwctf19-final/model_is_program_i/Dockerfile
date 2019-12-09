# stable-20191118
FROM debian@sha256:a1e12f1fc9804eda9b161c0c44d5438601f08f4af7fea1b4c4801d31f84f3635
RUN apt-get update && apt-get install -y musl-tools
WORKDIR /build
ADD readflag.c .
RUN musl-gcc -s -oreadflag -Os -static readflag.c

# ------------------------------------------------------------------------------

FROM dc2019f-ai-han-solo-service
ARG FLAG="rwctf{this_is_not_the_flag_on_server}"
ADD app.py /
EXPOSE 1337

COPY --from=0 --chown=1337:1337 /build/readflag /
RUN chmod u=srx,g=rx,o=x /readflag
RUN echo "${FLAG}" > /flag && chmod 0400 /flag && chown 1337:1337 /flag

USER nobody:nogroup
ENTRYPOINT [ "gunicorn3", "-b", "0.0.0.0:1337", "app:app" ]
