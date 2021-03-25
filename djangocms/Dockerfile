FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /djangocms
COPY requirements.txt /djangocms/
RUN pip install -r requirements.txt
COPY . /djangocms/