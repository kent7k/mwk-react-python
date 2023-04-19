# pull base image
FROM node:16.15.0-alpine

# set a work directory
WORKDIR /mwk/frontend

# install dependencies
COPY ./package.json .
COPY ./yarn.lock .
RUN yarn install

# copy app
COPY . .
