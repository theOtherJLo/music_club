FROM python:3.8
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8080
ENV DEBUG=*
ENV PYTHONPATH = $PYTHONPATH:/app/
CMD ["python", "main.py"]