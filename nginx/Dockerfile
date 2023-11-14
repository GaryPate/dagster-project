FROM nginx:1.21.3-alpine as base

ARG GFUSER
ARG GFPASS

ENV GF_SECURITY_ADMIN_USER=${GFUSER} 
ENV GF_SECURITY_ADMIN_PASSWORD=${GFPASS} 

# generate self segined certificate for testing pruposes
RUN apk update && \
    apk add --no-cache lsof && \
    apk add --no-cache bash && \
    apk add --no-cache openssl && \
    openssl req -x509 -nodes -days 365 \
    #-subj "/C=PL/ST=lubelskie/L=Lublin/O=github-rvva/OU=dev/CN=rvva" \
    -newkey rsa:4096 -keyout /etc/ssl/private/app.sentimax.org.key \
    -out /etc/ssl/certs/app.sentimax.org.crt


