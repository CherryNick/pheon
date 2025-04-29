ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim-bullseye AS base

ARG PIP_EXTRA_INDEX_URL
ARG UV_VERSION=0.6.2
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT="/usr/local"


RUN mkdir -p /code/
WORKDIR /code/

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get upgrade -y
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install uv==${UV_VERSION}

COPY pyproject.toml uv.* /code/

# Таргет для разработки, включающий dev зависимости
FROM base AS development

RUN uv sync --all-groups

COPY . /code/

CMD uvicorn src.main:app --host 0.0.0.0 --port=8080 --app-dir src

# Основной таргет, устанавливающий только необходимые зависимости
FROM base AS production

RUN uv sync --compile-bytecode --no-dev

COPY . /code/

CMD uvicorn src.main:app --host 0.0.0.0 --port=8080 --app-dir src