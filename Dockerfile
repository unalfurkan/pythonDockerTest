# docker build -t docker-test -f Dockerfile .
# docker run docker-test

FROM python:3
WORKDIR /usr/src/app
COPY . .
CMD ["helloWorld.py"]
ENTRYPOINT ["python3"]