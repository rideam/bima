FROM python:3.9-buster

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.


EXPOSE 8000
COPY requirements.txt .


RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

#CMD python3 app.py
CMD ["gunicorn"  , "--bind", "0.0.0.0:8000", "app:app"]