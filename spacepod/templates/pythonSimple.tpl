# Simple Python 3.7 program container
# Program: '{{ input("filename", "Python filename", None) }}'
FROM python:3.7-alpine as base
FROM base as builder

RUN mkdir /{{basename("filename")}}
WORKDIR /{{basename("filename")}}
ADD {{var("filename")}} /{{basename("filename")}}
CMD ["python", "/{{basename("filename")}}/{{var("filename")}}]
