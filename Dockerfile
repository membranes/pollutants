# Base Image
FROM python:3.11.6-bookworm

# pip
RUN pip install --upgrade pip

# If the steps of a `Dockerfile` use files that are different from the `context` file, COPY the
# file of each step separately; and RUN the file immediately after COPY
WORKDIR /app

COPY .devcontainer/requirements.txt /app
RUN pip install --requirement /app/requirements.txt --no-cache-dir

# Port
EXPOSE 8050

# ENTRYPOINT
ENTRYPOINT ["bash"]