FROM python:3.10-slim

WORKDIR /iot-device-status-sensor

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pytest unittests/test_validators.py routers/test_status.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
