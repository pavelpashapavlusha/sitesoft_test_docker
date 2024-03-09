FROM python:3.11.8


RUN mkdir /sitesoft_test


WORKDIR /sitesoft_test


COPY requirements.txt /sitesoft_test


RUN pip3 install -r /sitesoft_test/requirements.txt --no-cache-dir


COPY test_parser.py /sitesoft_test


COPY chromedriver /sitesoft_test


COPY parser_sitesoft_dj /sitesoft_test


COPY README /sitesoft_test


RUN cd parser_sitesoft_dj


RUN python3 manage.py makemigrations


RUN python3 manage.py migrate


RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('pavelmyskin', 'artem@gmail.com', '1731')" | python3 manage.py shell


RUN cd ..


RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable


RUN /usr/local/bin/python3 /sitesoft_test/test_parser.py


RUN cd parser_sitesoft_dj


CMD ["python3", "manage.py", "runserver", "0:8000"] 