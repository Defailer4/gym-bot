FROM ubuntu:latest
LABEL authors="itroc"

ENTRYPOINT ["top", "-b"]