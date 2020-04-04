FROM python:3.8-slim

ADD components/data_handler components/data_handler
RUN pip3 install -r components/data_handler/requirements.txt

ENTRYPOINT [ "entrypoint.sh" ]