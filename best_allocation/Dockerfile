FROM python:3.8.6-buster

copy api /api
copy data /data
copy requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.best_allocation:app --host 0.0.0.0 --port $PORT
