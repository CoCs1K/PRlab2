FROM python:3.9-slim

WORKDIR /service2app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "service2:app", "--host", "0.0.0.0", "--port", "8001"]
