FROM python:3.7-alpine3.8

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.8/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.8/community" >> /etc/apk/repositories

# upgrade and update VM
RUN apk upgrade
RUN apk update && apk add \
  bash openssh vim curl   \
  build-base git chromium \
  chromium-chromedriver   \
  gcc libxslt-dev         \
  --no-cache ca-certificates

FROM python:3.7

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

## Gecko Driver
#ENV GECKODRIVER_VERSION 0.23.0
#RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
#    && rm -rf /opt/geckodriver \
#    && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
#    && rm /tmp/geckodriver.tar.gz \
#    && mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
#    && chmod 777 /opt/geckodriver-$GECKODRIVER_VERSION \
#    && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/geckodriver \
#    && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/wires

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install xvfb
RUN apt-get install -yqq xvfb

# install pip
RUN curl -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install --upgrade pip

# copy source code
COPY . project
RUN pwd && ls -la

# install requirements
RUN pip install virtualenv
RUN virtualenv venv
# RUN source ./venv/bin/activate
RUN pip install -r project/requirements.txt

# Grand permissions
RUN chmod -R 775 project/src/drivers

# set display port to avoid crash
ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null

# Leave it on
CMD tail -f /dev/null
