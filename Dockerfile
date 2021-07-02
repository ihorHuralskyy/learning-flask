FROM python:3.8.10
ENV FLASK_APP "hello_books"
ADD . /flaskdocker
WORKDIR /flaskdocker
RUN pip install -r requirements.txt
