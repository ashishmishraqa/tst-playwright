FROM python:3.11-slim

# Set working directory
WORKDIR /automation

# ═══════════════════════════════════════════════════════════════════════
# LAYER 1: System dependencies (rarely changes)
# ═══════════════════════════════════════════════════════════════════════
RUN apt-get update && apt-get install -y \
    default-jre \
    wget \
    && rm -rf /var/lib/apt/lists/*

# ═══════════════════════════════════════════════════════════════════════
# LAYER 2: Allure CLI (rarely changes - pin to specific version)
# ═══════════════════════════════════════════════════════════════════════
RUN wget -q https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz && \
    tar -zxf allure-2.27.0.tgz -C /opt/ && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure && \
    rm allure-2.27.0.tgz

# ═══════════════════════════════════════════════════════════════════════
# LAYER 3: Python dependencies (changes when requirements.txt changes)
# Copy requirements ONLY first, so this layer caches independently
# ═══════════════════════════════════════════════════════════════════════
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir boto3

# ═══════════════════════════════════════════════════════════════════════
# LAYER 4: Playwright browsers (takes time, but stable)
# Only re-runs if requirements.txt changes (Playwright version)
# ═══════════════════════════════════════════════════════════════════════
RUN playwright install

# ═══════════════════════════════════════════════════════════════════════
# LAYER 5: Project code (changes frequently - goes LAST)
# This ensures code changes don't invalidate all previous layers
# ═══════════════════════════════════════════════════════════════════════
COPY . .

# Default command - runs tests with Allure reporting
CMD ["pytest", "ecart/tests", "-v", "--alluredir=allure-results"]