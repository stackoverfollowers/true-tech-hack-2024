ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim
ARG APP_YOLO_MODEL_PATH=./yolo.pt
ARG APP_YOLO_MODEL_URL

RUN apt update && apt install curl libgl1 libglib2.0-0 -y

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

ARG UID=1001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN pip install -U --no-cache-dir poetry pip && poetry config virtualenvs.create false

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    poetry install --no-interaction --no-ansi --no-root --without dev

RUN curl ${APP_YOLO_MODEL_URL} -o ./${APP_YOLO_MODEL_PATH}
ENV APP_YOLO_MODEL_PATH=$APP_YOLO_MODEL_PATH


COPY ./tth ./tth

EXPOSE 8000

CMD ["python", "-m", "tth.yolo"]