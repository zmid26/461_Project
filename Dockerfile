# Flask App
FROM python:3.10-slim-buster
WORKDIR /flask-app
COPY src/APIs/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 8080
ENV PORT 8080
COPY src/APIs/auth.py app.py
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
# CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]

# React App
# FROM node:14-alpine
# WORKDIR /react-app
# COPY react_app/package*.json ./
# RUN npm install --only=production
# COPY . .
# RUN npm run build
# EXPOSE 1234
# CMD ["npm", "start"]