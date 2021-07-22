FROM python:3.7

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update && apt-get install -y netcat

# create an app user in the app group
RUN useradd --user-group --create-home --no-log-init --shell /bin/bash/ app

ENV APP_HOME=/home/RecipeTracks

# Create static directory
RUN mkdir -p $APP_HOME/static

WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install Pillow

COPY . $APP_HOME 
RUN chown -R app:app $APP_HOME

USER app:app

ENTRYPOINT [ "./entrypoint.sh" ]