# Use an official Python runtime as a parent image
FROM python:3.12-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed by Playwright
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       wget \
       gnupg \
       libnss3 \
       libatk1.0-0 \
       libatk-bridge2.0-0 \
       libcups2 \
       libdrm2 \
       libxkbcommon0 \
       libxcomposite1 \
       libxrandr2 \
       libasound2 \
       libpangocairo-1.0-0 \
       libxshmfence1 \
       libxdamage1 \
       libgbm1 \
       libpango-1.0-0 \
       fonts-liberation \
       libgtk-3-0 \
       libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files to the working directory
COPY . /app/

# Install Python dependencies (including Playwright)
RUN pip install --no-cache-dir playwright

# Install Playwright browsers (e.g., Chromium)
RUN playwright install --with-deps chromium

# Set the command to run your Python script
CMD ["python", "asus_router_client_list.py"]
