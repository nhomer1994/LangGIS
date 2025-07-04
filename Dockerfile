FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME for PySpark
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Copy and install requirements first for layer caching
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source code into container
COPY src/ /app/src/
COPY notebooks/ /app/notebooks/
COPY data/ /app/data/
COPY app.py /app/app.py

# Default: run Streamlit app 
ENTRYPOINT ["streamlit", "run", "src/app.py"]
