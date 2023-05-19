FROM alpine:3.14

WORKDIR /usr/src/app

COPY app.py .

RUN apk add python3
RUN apk add py3-pip
RUN pip3 install flask


CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000/tcp
