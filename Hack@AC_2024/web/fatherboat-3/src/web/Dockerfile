FROM python:3.11.0-slim

WORKDIR /app

COPY requirements.txt .

COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "/app/app.py"]
