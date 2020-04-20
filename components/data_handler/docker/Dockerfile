FROM python:3.8-slim


COPY components/data_handler/ data_handler/

RUN pip install -r data_handler/requirements.txt

CMD python -u data_handler/data_handler.py