FROM python:3.10.1

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
RUN python -m pip install grpcio
CMD ["python", "/app/cf_service.py"]