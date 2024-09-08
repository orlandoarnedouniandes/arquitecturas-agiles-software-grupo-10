FROM python:3.10
WORKDIR /locust

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

EXPOSE 8089

ENV LOCUST_FILE=/app/locustfile.py

CMD ["locust", "-f", "/app/locustfile.py", "--host", "http://localhost:8089"]