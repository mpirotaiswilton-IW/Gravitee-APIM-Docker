FROM python:3-alpine

COPY init_gravitee.py /opt/init_gravitee.py

ADD /api-specs /opt/api-specs

WORKDIR /opt

USER root
RUN python -m pip install --upgrade pip
RUN python -m pip install requests
USER 1001

ENTRYPOINT [ "python", "/init_gravitee.py" ]