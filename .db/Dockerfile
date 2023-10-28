FROM mariadb:latest

WORKDIR /root/usr/database

ADD db.cnf /etc/mysql/conf.d/my.cnf

ADD ./init.sql /docker-entrypoint-initdb.d/

RUN chmod 644 /etc/mysql/my.cnf

EXPOSE 3306