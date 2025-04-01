FROM his-backlink:v1
#RUN apk update && apk add cron
COPY crontab.txt /his-backlink/crontab.txt
RUN chmod +x /his-backlink/schedule.sh
RUN crontab /his-backlink/crontab.txt

CMD ["crond", "-f"]
