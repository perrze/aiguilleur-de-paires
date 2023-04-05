FROM python:latest
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ADD ./orchestrator_main.py /opt/
EXPOSE 13000
EXPOSE 5000
CMD python3 /opt/orchestrator_main.py

