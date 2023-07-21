FROM registry.access.redhat.com/ubi8/python-39

ENV POETRY_VERSION=1.5.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

COPY {POETRY_VENV} {POETRY_VENV}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /usr/src/app

COPY ./src .
COPY ./schema.sql .
COPY . .

RUN poetry install --no-interaction --no-cache --without dev

CMD ["poetry", "run", "python", "-m", "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000/tcp
