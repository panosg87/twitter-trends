FROM python:3.6-slim

COPY ./web-api app/

RUN pip3 install -r /app/requirements.txt

EXPOSE 5000

CMD ["python3", "/app/src/api.py"]
