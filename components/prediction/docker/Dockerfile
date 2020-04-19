FROM python:3.8-slim

COPY components/prediction/ prediction/
COPY components/prediction/docker/entrypoint.sh .

RUN pip install -r prediction/requirements.txt

ENTRYPOINT [ "./entrypoint.sh" ]