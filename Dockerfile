FROM python:slim

RUN useradd upload

WORKDIR /home/upload

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY upload.py config.py boot.sh flask_celery.py ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R upload:upload ./
USER upload

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]