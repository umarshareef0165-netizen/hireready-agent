FROM python:3.12-slim
WORKDIR /app
COPY . /app
EXPOSE 8002
CMD ["sh", "-c", "python3 src/server.py"]
