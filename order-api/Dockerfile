FROM python:3.11

COPY /app /app
COPY pyproject.toml /app 

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only main

CMD ["uvicorn", "main:app"]
