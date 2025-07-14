FROM python:3.12-slim

# Non-interactive frontend to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        borgbackup \
        openssh-client \
        iputils-ping \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install requirements file
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY src/ src/

# Default startup command
CMD ["python", "src/main.py"]
