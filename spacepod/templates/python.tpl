# Simple Python 3.7 program with HTTP port exposed
# Program: '{{ input("filename", "Python filename", None) }}'
FROM python:3.7-alpine as base
FROM base as builder

RUN mkdir /{{basename("filename")}}
WORKDIR /{{basename("filename")}}
ADD {{var("filename")}} /{{basename("filename")}}
EXPOSE {{var("port",8080)}}
CMD ["python", "/{{basename("filename")}}/{{var("filename")}}]
