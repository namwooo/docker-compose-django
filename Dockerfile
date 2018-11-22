FROM        base
MAINTAINER  garson13@g62mail.com

ENV         LANG C.UTF-8
ENV         DJANGO_SETTINGS_MODULE config.settings

# requirement
COPY        . /srv/app
RUN         /root/.pyenv/versions/app/bin/pip install -r \
            /srv/app/requirements.txt

WORKDIR     /srv/app
RUN         pyenv local app

# nginx
RUN         cp /srv/app/.config/nginx/debug.conf \
                /etc/nginx/nginx.conf

RUN         cp /srv/app/.config/nginx/app.conf \
                /etc/nginx/sites-available/
RUN         rm -rf /etc/nginx/sites-enabled/*
RUN         ln -sf /etc/nginx/sites-available/app.conf \
                    /etc/nginx/sites-enabled/app.conf

# uWSGI
RUN         mkdir -p /var/log/uwsgi/app
RUN         mkdir -p /tmp/uwsgi


# manage.py
WORKDIR     /srv/app/handys
RUN         /root/.pyenv/versions/app/bin/python manage.py collectstatic --noinput

# postgres
RUN         echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf

# supervisor
RUN         cp /srv/app/.config/supervisor/* \
                /etc/supervisor/conf.d

CMD         supervisord -n

EXPOSE      80