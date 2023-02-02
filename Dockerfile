FROM python:3.10.9-alpine3.17
WORKDIR /app/backend

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 4000
CMD ["python", "main.py"]