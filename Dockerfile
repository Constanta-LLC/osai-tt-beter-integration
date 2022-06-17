FROM python:3.10.2-slim-bullseye
RUN pip install signalrcore
RUN pip install tabulate
WORKDIR /app
COPY client.py .
ENTRYPOINT [ "python", "client.py" ]