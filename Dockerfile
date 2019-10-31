FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir .

EXPOSE 9410

CMD [ "bash" ]
