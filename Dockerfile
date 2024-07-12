From nanozoo/python3.12

add cmd/nsc_docker usr/bin/nsc
RUN chmod 777 /usr/bin/nsc

ADD app /project/app
ADD tests /project/tests
ADD setup.cfg /project/
#ADD start.sh /project/start.sh

RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' etc/apt/sources.list
RUN apt-get -y update
RUN apt-get -y install libblas-dev liblapack-dev selinux-utils setools uwsgi net-tools locales vim apt-transport-https ca-certificates pkg-config gcc libc-dev make wget curl git libssl-dev libsasl2-dev libzstd-dev

COPY ./requirements.txt /project/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /project/app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

WORKDIR /project
RUN python -m coverage run -m pytest
RUN python -m coverage report

ARG GIT_BRANCH
ARG BUILD_NUMBER
ARG GIT_COMMIT
ARG TIMESTAMP

RUN echo "{\"branch\":\"$GIT_BRANCH#$BUILD_NUMBER\",\"commit\":\"$GIT_COMMIT\",\"timestamp\":\"$TIMESTAMP\"}" > /buildinfo.json
CMD ["uvicorn", "app.main:start_app", "--host", "0.0.0.0", "--port", "80", "--workers", "1", "--limit-max-requests", "500", "--timeout-keep-alive", "5", "--ws-max-size", "2097152"]