FROM python:3.9.5

EXPOSE 8000

COPY . /apps/webshop
WORKDIR /apps/webshop

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=webshop.settings.dev

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxtst6 \
    xdg-utils \
    wkhtmltopdf \
    gettext \
  && rm -rf /var/lib/apt/lists/*

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb

RUN pip3 install -r /apps/webshop/requirements/dev.txt

CMD python manage.py migrate --noinput; python manage.py runserver 0.0.0.0:8000
