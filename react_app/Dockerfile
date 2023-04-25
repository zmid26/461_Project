FROM node:16-alpine
WORKDIR /react-app
COPY package*.json ./
RUN npm install --only=production
COPY . .
RUN npm run build
EXPOSE 1234
ENV REACT_APP_SERVER_URL https://react-front-end-fgnl7r7dtq-uc.a.run.app
CMD ["npm", "run", "start"]

# COPY react_app/package*.json ./
#  --openssl-legacy-provider