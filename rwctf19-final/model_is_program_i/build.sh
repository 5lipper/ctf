#!/bin/bash -e

UPSTREAM_REPO=https://github.com/o-o-overflow/dc2019f-ai-han-solo-public.git
COMMIT=1f53bb2dee12440b6971f8a9cbf33d3d4214deea
docker build -t dc2019f-ai-han-solo-service "$UPSTREAM_REPO#$COMMIT:service"

rm -rf out || true
mkdir -p out/public

docker build -t model-is-program-1:public .
docker build -t model-is-program-1:prod --build-arg FLAG=$(cat flag) .
docker save model-is-program-1:public -o out/public/image.tar
docker save model-is-program-1:prod | gzip -n > out/prod-image.tar.gz

tar --sort=name \
    --owner=0 --group=0 --numeric-owner \
    --mtime="@${SOURCE_DATE_EPOCH}" \
    -cvf out/release.tar \
    build.sh Dockerfile readflag.c app.py out/public
mv out/prod-image.tar.gz out/prod-image.tar.gz.$(sha256sum out/prod-image.tar.gz | awk '{print $1}')
mv out/release.tar out/release.tar.$(sha256sum out/release.tar | awk '{print $1}')
gzip -n out/release.tar.*
