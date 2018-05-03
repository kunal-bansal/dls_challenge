FROM python:3

COPY . /app
WORKDIR /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python"]
CMD ["-u","main.py"]