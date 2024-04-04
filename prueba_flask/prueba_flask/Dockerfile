FROM python:3.9-slim

WORKDIR /app

COPY app.py /app/
COPY requirements.txt /app/

EXPOSE 5001

RUN pip install -r requirements.txt

CMD ["python", "app.py"]

