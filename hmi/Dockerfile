FROM grafana/grafana:13.0.0-23336907879-ubuntu

USER root

RUN apt-get update && apt-get install -y gettext-base
RUN grafana cli plugins install volkovlabs-form-panel
RUN grafana cli plugins install marcusolsson-dynamictext-panel

USER grafana