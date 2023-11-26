FROM grafana/grafana-enterprise

ARG GFUSER
ARG GFPASS

ENV RESET_ADMIN_PASSWORD=${GFPASS} 
RUN echo $RESET_ADMIN_PASSWORD

CMD ["grafana-cli", "admin", "reset-admin-password", "echo ${RESET_ADMIN_PASSWORD}"]

ENV GF_INSTALL_PLUGINS=grafana-bigquery-datasource