# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN python -m pip install gradio
RUN python -m pip install requests

WORKDIR /app
COPY ./demoAI2.py /app
COPY ./inst.txt /app 
COPY ./inst_ocr.txt /app
COPY ./llama3.png /app


EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "demoAI2.py"]
