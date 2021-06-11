FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY schema.sql ./
COPY csv_data/ csv_data/

CMD [ "python", "./CSV_source.py" ]