FROM python:3.9.12-slim

RUN pip install fastapi uvicorn poetry wheel virtualenv

EXPOSE 8000

WORKDIR /usr/src/projectname

ENV PORT 8000
ENV HOST "0.0.0.0"COPY ./src/ /projectname/src
COPY ./main.py /projectname
COPY ./pyproject.toml /projectname

WORKDIR /projectnameRUN poetry config virtualenvs.create false \
  && poetry install

CMD ["uvicorn", "main:app"]
