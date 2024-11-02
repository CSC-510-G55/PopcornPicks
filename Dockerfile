FROM node:latest AS react-build

WORKDIR /frontend

COPY ./react-frontend /frontend

RUN npm install --force
RUN npm run build

FROM python:3.9

WORKDIR /app

COPY --from=react-build /frontend/build /app/react-frontend/build

COPY ./requirements.txt /app/
COPY ./src /app/src
COPY ./data /app/data

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y npm && npm install -g serve

EXPOSE 3000 5000

CMD ["sh", "-c", "cd react-frontend/build && serve -s . -l 3000 --single & python -m src.recommenderapp.app"]