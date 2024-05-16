# Server

FROM python:3.8.5

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get install iproute2
COPY . /app/
COPY container_init.sh /container_init.sh

EXPOSE 8765

ENTRYPOINT [ "/bin/bash" ]


