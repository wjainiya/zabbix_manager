# FOR 10.10.2.86:5000/zabbix_report_v1

FROM python:2.7
RUN apt-get update && apt-get install -y vim && apt-get clean
RUN pip install zabbix-api pytz python-dateutil matplotlib requests pillow
# 改变代码目录为code
COPY ./code /code
WORKDIR /code
RUN bash start.sh
ENV EDITOR=vim
ENTRYPOINT tail -f /dev/null

