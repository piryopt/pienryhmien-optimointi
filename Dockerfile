FROM python:3.9

WORKDIR /usr/src/app

#ENV DATABASE_URL=postgresql://username:password@possu.it.helsinki.fi/KANTA?ssl=true:5432/piryopt

ENV_FILE .env

COPY ./src .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN export $(cat $ENV_FILE | xargs)

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000/tcp
