FROM python:3.8-slim

COPY components/data_handler/ data_handler/
COPY components/data_handler/docker/entrypoint.sh .

RUN pip3 install -r data_handler/requirements.txt

ENTRYPOINT [ "./entrypoint.sh" ]