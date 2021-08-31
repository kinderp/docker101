FROM ubuntu

RUN apt update -y

RUN apt install -y incron vim curl

RUN echo "root" > /etc/incron.allow

#RUN echo '/shared IN_CLOSE_WRITE echo IN_CLOSE_WRITE >> /tmp/$#' >> /var/spool/incron/root
RUN echo '/shared IN_CLOSE_WRITE /tools/notifier.sh $#' >> /var/spool/incron/root

ENV INTERFACE_HOST=interface

COPY notifier.sh /tools/notifier.sh

RUN chmod 777 /tools/notifier.sh

#CMD ["sleep", "100000"]
CMD ["incrond", "--foreground"]




