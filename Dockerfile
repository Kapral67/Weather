FROM nginx:latest
RUN rm /etc/nginx/conf.d/default.conf
WORKDIR /app/
COPY ./blazor-wasm/weatherFrontEnd/bin/Release/net6.0/publish/wwwroot/ /app/
COPY nginx/sites-enabled /etc/nginx/conf.d
RUN mkdir /etc/nginx/ssl
COPY nginx/ssl/ /etc/nginx/ssl/
