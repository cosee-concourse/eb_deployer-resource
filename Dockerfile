FROM ruby:2.2-alpine

# SET eb_deployer Version like
# docker build --build-arg ebdeployerVersion=0.6.6
ARG ebdeployerVersion=0.6.6

RUN mkdir -p /aws && \
    apk -Uuv add python3 git && \
    rm /var/cache/apk/* && \
    gem install eb_deployer -v $ebdeployerVersion

COPY opt /opt

RUN pip3 install -r /opt/requirements.txt
