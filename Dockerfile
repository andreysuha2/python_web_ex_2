FROM python:3.11

ENV APP_HOME=/app \
    POETRY_VERSION=1.6.1

WORKDIR $APP_HOME

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY . .

ENTRYPOINT [ "poetry", "run", "python", "-u", "main.py" ]