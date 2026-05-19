FROM python:3.11-slim

# Set working directory
WORKDIR /automation

# Install system dependencies (Java for Allure CLI)
RUN apt-get update && apt-get install -y \
    default-jre \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Allure CLI
RUN wget -q https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz && \
    tar -zxf allure-2.27.0.tgz -C /opt/ && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure && \
    rm allure-2.27.0.tgz

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir boto3

# Install Playwright browsers
RUN playwright install

# Copy project files
COPY . .

# Default command - runs tests with Allure reporting
CMD ["pytest", "ecart/tests", "-v", "--alluredir=allure-results"]