FROM node:18-bullseye

WORKDIR /app

RUN corepack enable && corepack prepare yarn@stable --activate

COPY package*.json ./
RUN rm -f package-lock.json
RUN yarn cache clean
RUN yarn install --frozen-lockfile --network-timeout 600000 || yarn install

COPY . .
RUN yarn build
RUN yarn global add serve

EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]

