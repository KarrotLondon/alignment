FROM python:3.10 as base

WORKDIR /app

RUN apt-get update && apt-get -y install \
    # Poetry install deps
    curl

ENV POETRY_VERSION=1.1.13
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="/root/.poetry/bin:${PATH}"

COPY run.sh ./run.sh
RUN chmod +x ./run.sh

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
RUN poetry config virtualenvs.create false


EXPOSE 8080
RUN poetry install --no-dev --no-root
RUN poetry add gunicorn
COPY src ./src

CMD ["./run.sh"]