FROM python:3.10
EXPOSE 8080

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install flask

CMD ["python3", "app.py"]
