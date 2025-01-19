FROM python:3.10

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install flask
RUN pip install lxml==4.9.3

CMD ["python3", "app.py"]
