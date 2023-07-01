FROM python:3.11-slim

COPY ./ /app

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only main

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
