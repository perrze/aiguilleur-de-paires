# syntax=docker/dockerfile:1
FROM debian
ENV ORCHIP=127.0.0.1
RUN apt update
RUN apt install -y python3 python3-serial
RUN apt clean
ADD ./main.py /opt/main.py
ADD ./phantom_switchman.py /opt/phantom_switchman.py
CMD python3 /main.py

