FROM python:3.12.2-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 80

CMD ["sh","-c","streamlit run app/app.py --server.port 80 & uvicorn app.main:app --host 0.0.0.0 --port 8080"]