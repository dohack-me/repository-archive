FROM python:3.9
EXPOSE 5050

WORKDIR /app
COPY build /app
RUN pip install flask
CMD ["python", "main.py"]