FROM python:3.10
EXPOSE 8080

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

CMD ["python3", "app.py"]
