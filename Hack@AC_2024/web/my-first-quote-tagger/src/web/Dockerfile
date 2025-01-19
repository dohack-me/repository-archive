FROM python:3.11

WORKDIR /app
COPY app.py .
COPY stuffs stuffs
COPY requirements.txt .

RUN mkdir signed_files

RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["gunicorn", "-w", "5", "-b", "0.0.0.0", "app:app"]
