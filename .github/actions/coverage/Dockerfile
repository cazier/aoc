FROM alpine:latest

RUN apk add curl gpgv gnupg coreutils

COPY entrypoint.sh /bin/entrypoint.sh

ENTRYPOINT ["/bin/entrypoint.sh"]
