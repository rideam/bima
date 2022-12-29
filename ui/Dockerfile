FROM node:lts-alpine as build-stage

WORKDIR /app

#ENV PATH /app/node_modules/.bin:$PATH

#RUN npm install -g @vue/cli

COPY package.json .
COPY yarn.lock .
RUN yarn install
COPY . .
RUN yarn run build

CMD ["yarn", "run", "dev"]


# Production stage
FROM nginx:1.16.1-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD [ "nginx", "-g", "daemon off;"]