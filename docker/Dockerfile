FROM python:3.8

RUN adduser api_flask

WORKDIR /home/api_flask

COPY docker/requirements.txt ./
RUN python3 -m venv venv
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install gunicorn

COPY app app
COPY tests tests
COPY migrations migrations
COPY config.py models.py schemes.py ./

COPY docker/boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP app

RUN chown -R api_flask:api_flask ./
USER api_flask

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
