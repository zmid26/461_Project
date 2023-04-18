# Flask App
FROM python:3.10-slim-buster
WORKDIR /flask-app
COPY src/APIs/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 8080
COPY src/APIs/app.py app.py
CMD [ "python3", "app.py"]

# React App
# FROM node:14-alpine
# WORKDIR /react-app
# COPY react_app/package*.json ./
# RUN npm install --only=production
# COPY . .
# RUN npm run build
# EXPOSE 1234
# CMD ["npm", "start"]