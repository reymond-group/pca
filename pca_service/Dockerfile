FROM python:3

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
COPY . .

RUN mkdir -p /models

CMD [ "python", "./planes.py", "/models" ]

EXPOSE 80
