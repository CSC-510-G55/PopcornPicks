FROM python:3.9

ARG MONGO_URI

ENV MONGO_URI=$MONGO_URI

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY ./recommenderapp /app/src/recommenderapp

EXPOSE 5001

CMD ["python", "-m", "src.recommenderapp.app"]