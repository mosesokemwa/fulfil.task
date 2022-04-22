FROM python:slim

RUN useradd upload

COPY . /home/upload

WORKDIR /home/upload

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn
RUN venv/bin/pip install celery

COPY wsgi.py app.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R upload:upload ./
USER upload

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]