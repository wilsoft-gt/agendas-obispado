#Docker image to use
FROM python:3.10.6-alpine3.16

#Defines the working directory for the app
WORKDIR /app/

#Copy all files to the app folder
COPY . /app/

#Defines ENV Variables
ENV SECRET_KEY="8pxb@6g%hn$z(c$i0ozignb_zmx(*ips$x*7cvze!n*j7+2oov"
ENV IS_DEBUG="False"

#Required for python createuser --noinput
ENV DJANGO_SUPERUSER_EMAIL="admin@admin.com"
ENV DJANGO_SUPERUSER_USERNAME="wilsoft"
ENV DJANGO_SUPERUSER_PASSWORD="admin123."

#Install dependencies
RUN apk add gcc python3-dev jpeg-dev zlib-dev musl-dev mysql-client
RUN pip install -r requirements.txt

#Generate database tables and superuser
RUN python manage.py migrate
RUN python manage.py makemigrations
RUN python manage.py createsuperuser --noinput
RUN python manage.py collectstatic --noinput

#Start the server
CMD [ "gunicorn", "whatsapp.wsgi:application" ]







