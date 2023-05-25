# Use the official Python image as the base image
FROM python:3.9

WORKDIR /usr/src/app

COPY ./src .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000/tcp
