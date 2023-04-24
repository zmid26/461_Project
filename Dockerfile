# Flask App
FROM python:3.10-slim-bullseye
WORKDIR /flask-app
COPY gcp.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 8080
COPY app.py .
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]
# CMD ["python", "app.py"]
# COPY src/APIs/requirements.txt requirements.txt
# COPY src/APIs/app.py app.py

# React App
# FROM node:14-alpine
# WORKDIR /react-app
# COPY react_app/package*.json ./
# RUN npm install --only=production
# COPY . .
# RUN npm run build
# EXPOSE 1234
# CMD ["npm", "start"]