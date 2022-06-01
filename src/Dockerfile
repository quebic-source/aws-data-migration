FROM python:3.11.0b1-alpine3.16

ARG SRC_DIR

WORKDIR /code

COPY ${SRC_DIR}/. /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["python", "main.py"]