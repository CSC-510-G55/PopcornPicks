# Stage 1: Build React App
FROM node:latest AS react-build

WORKDIR /frontend

# Copy React app code
COPY ./react-frontend /frontend

# Install dependencies and build the React app
RUN npm install
RUN npm run build

# Stage 2: Final Stage with both React and Flask
FROM python:3.9

WORKDIR /app

# Copy the built React files from the build stage
COPY --from=react-build /frontend/build /app/react-frontend/build

# Copy all backend files
COPY ./requirements.txt /app/
COPY ./src /app/src
COPY ./data /app/data

# Install Python dependencies
RUN pip install -r requirements.txt

# Install serve globally for serving the React app
RUN apt-get update && apt-get install -y npm && npm install -g serve

# Expose ports for React and Flask
EXPOSE 3000 5001

# Run both Flask and React servers
# Change this line in your Dockerfile
CMD ["sh", "-c", "cd react-frontend/build && serve -s . -l 3000 --single & python -m src.recommenderapp.app"]