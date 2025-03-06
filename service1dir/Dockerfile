FROM python:3.9-slim

WORKDIR /service1app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "service1:app", "--host", "0.0.0.0", "--port", "8000"]
