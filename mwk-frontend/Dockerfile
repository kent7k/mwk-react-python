FROM node:16.15.0-alpine

WORKDIR /mwk/frontend

COPY ./package.json .
COPY ./yarn.lock .
RUN yarn install && yarn cache clean
COPY . .

RUN yarn build && rm -rf node_modules
CMD ["yarn", "start"]
