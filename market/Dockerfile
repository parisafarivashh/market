FROM python:3.9.6-alpine

# set work directory
WORKDIR /home/parisa/Desktop/market/market

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /home/parisa/Desktop/market/market/entrypoint.sh
RUN chmod +x /home/parisa/Desktop/market/market/entrypoint.sh


# copy project
COPY . .


# run entrypointprod.sh
ENTRYPOINT ["/home/parisa/Desktop/market/market/entrypoint.sh"]