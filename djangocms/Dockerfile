FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /djangocms
COPY requirements.txt /djangocms/
RUN pip3 install -r requirements.txt
COPY . /djangocms/
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]