# Project Documentation for Router Scraper

## Overview
The Router Scraper is a Python application designed to scrape client information from an ASUS router. It utilizes Playwright for web automation and provides a simple way to retrieve connected device details.

## Compatibility
Any ASUS router currently supported and running Asus-Merlinwrt

## Project Structure
```
router-scraper
├── src
│   ├── asus_router_client_list.py
│   └── find_router_ip.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

## Requirements
- Python 3.x
- Docker
- Docker Compose

## Setup Instructions

### 1. Credentials
Modify the `.env` file in the root directory and add your router credentials:
```
ROUTER_USER=your_username
ROUTER_PASS=your_password
```

### 2. Build the Docker Image
Run the following command to build the Docker image:
```bash
docker-compose build
```

### 3. Run the Application
To start the application, use:
```bash
docker-compose up
```

### 4. Accessing the Scraper
The scraper will run and output the client list to the console. Ensure your router is accessible from the Docker container.

## Notes
- Ensure that the router's web interface is reachable from the Docker container.
- Modify the `docker-compose.yml` file if you need to change any service configurations.