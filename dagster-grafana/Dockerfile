FROM grafana/grafana-enterprise

ARG GFUSER
ARG GFPASS

#ENV GF_SECURITY_ADMIN_USER=${GFUSER} 
ENV RESET_ADMIN_PASSWORD=${GFPASS} 
RUN echo $RESET_ADMIN_PASSWORD
# ENV GF_PATHS_CONFIG = /usr/grafana/grafana.ini

# CMD ["dagster-webserver", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]
CMD ["grafana-cli", "admin", "reset-admin-password", "echo ${RESET_ADMIN_PASSWORD}"]
#ENV GF_SERVER_DOMAIN = app.sentimax.org
#ENV GF_SERVER_HTTP_PORT = 3010
#ENV GF_SERVER_ROOT_URL = "http://app.sentimax.org/grafana/"
#ENV GF_SERVER_SERVE_FROM_SUB_PATH = true

# ENV GF_SERVER_ROOT_URL = %(protocol)s://%(domain)s:%(http_port)s/grafana/
# ENV GF_SERVER_SERVE_FROM_SUB_PATH = true

# COPY . .

# ENV DAGSTER_POSTGRES_USER=${PGUSER}

# ENV POSTGRES_DB=dagsterdb 
# ENV POSTGRES_PASSWORD=${PGPASS}
# ENV POSTGRES_USER=${PGUSER}

# RUN echo $POSTGRES_USER
# RUN echo $POSTGRES_PASSWORD
# RUN echo $POSTGRES_DB

ENV GF_INSTALL_PLUGINS=grafana-bigquery-datasource