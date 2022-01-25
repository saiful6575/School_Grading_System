# pull image
FROM node:12.20.1-alpine3.10

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# Install library dependencies
RUN apk add bash \
    autoconf \
    automake \
    g++ \
    libc6-compat \
    libjpeg-turbo-dev \
    libpng-dev \
    make \
    nano \
    nasm

RUN rm -rf /tmp/* /var/cache/apk/*


# add app
COPY . ./

#RUN npm install --silent
RUN npm install --unsafe-perm
# RUN npm install