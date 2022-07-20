FROM python:3.10-bullseye

WORKDIR /app

COPY ./requirements.txt ./

RUN pip3 install --upgrade pip --no-cache-dir && pip3 install -r requirements.txt --no-cache-dir


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
