FROM python:3.6.1-alpine
ADD . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python", "app.py"]