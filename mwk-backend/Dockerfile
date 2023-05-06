FROM python:3.11.3-alpine

WORKDIR /mwk/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install ruamel_yaml dependency
RUN apk add --no-cache \
    gcc musl-dev python3-dev \
    libxml2-dev libxslt-dev \
    jpeg-dev zlib-dev libjpeg \
    libffi-dev
# --- Note about dependencies ---
# lxml: libxml2-dev libxslt-dev
# Pillow: jpeg-dev zlib-dev libjpeg
# cffi: libffi-dev
# -------------------------------

RUN pip install --upgrade pip
COPY ./requirements ./requirements
RUN pip install \
		--requirement requirements/constraints.txt \
		--requirement requirements/base.txt \
		--requirement requirements/common.txt \
		--requirement requirements/dev.txt
# TODO: changet to `-c constrains.txt`
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

COPY . .

# copy entrypoint.sh & execute
COPY resources/entrypoint.sh .
RUN sed -i 's/\r$//g' /mwk/backend/entrypoint.sh
RUN chmod +x /mwk/backend/entrypoint.sh
ENTRYPOINT ["/mwk/backend/entrypoint.sh"]
