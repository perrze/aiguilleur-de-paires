# syntax=docker/dockerfile:1
FROM debian
RUN apt update
RUN apt install -y python3
RUN apt clean
ADD ./main.py /main.py
EXPOSE 13130
EXPOSE 13000
CMD python3 /main.py

