FROM python:3
WORKDIR /whoplayer

# Installing dependencies
COPY requirments.txt ./
RUN pip install --no-cache-dir -r requirments.txt

# Copy server files
RUN mkdir /app
COPY ./app/* /app
EXPOSE 8081

CMD ["fastapi", "run", "/app/main.py", "--port", "8081"]

# CMD ls AppBackend/DownloadServer
  

