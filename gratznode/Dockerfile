FROM node:lts-slim

RUN apt-get update && \
    apt-get install -qqy --no-install-recommends \
    dumb-init && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

COPY ./package* ./
COPY ./*.js ./

RUN npm ci
RUN chown -R node /app/

EXPOSE 3030

USER node

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["node", "best.js"]


