FROM python:3.9

ARG MONGO_URI
ARG OMDB_API_KEY
ARG WATCHMODE_API_KEY

ENV MONGO_URI=$MONGO_URI
ENV OMDB_API_KEY=$OMDB_API_KEY
ENV WATCHMODE_API_KEY=$WATCHMODE_API_KEY

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY ./recommenderapp /app/backend/recommenderapp

EXPOSE 5001

CMD ["python", "-m", "backend.recommenderapp.app"]