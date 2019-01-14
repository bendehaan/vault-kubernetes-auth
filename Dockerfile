FROM python:3.6-alpine

LABEL maintainer="bdehaan@xebia.com"

RUN pip3 install hvac

COPY vault_test.py /opt/vault_test.py

USER nobody

ENTRYPOINT ["/usr/local/bin/python3.6", "/opt/vault_test.py"]
