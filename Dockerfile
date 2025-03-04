FROM python:3.12.2-alpine3.19

WORKDIR /usr/src/app

EXPOSE 8000

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python -m certify
