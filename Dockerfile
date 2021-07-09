FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN python3 -m pip install -r requirements.txt
# Adding manual Pillow install because locally we use the binary/wheel version of Pillow
RUN python3 -m pip install Pillow
COPY . /code/
# Database setup
RUN python3 manage.py makemigrations --noinput
RUN python3 manage.py migrate --noinput

EXPOSE 8000
# Running the actual server (test version - NOT PROD)
CMD python3 manage.py runserver 0.0.0.0:8000
