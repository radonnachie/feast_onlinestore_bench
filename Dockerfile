FROM python:3.8

WORKDIR /work/

RUN pip install couchbase pandas
RUN pip install git+https://github.com/radonnachie/feast@couchbase_onlinestore

COPY . /work/

RUN /bin/bash -c "cd /work/store/data/ && python ./generate.py"
