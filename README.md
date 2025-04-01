# Backlink Detection and Monitoring System

## Overview
The Backlink Detection and Monitoring System is an automated tool designed to detect and monitor backlinks pointing to government websites in Vietnam. This project specifically targets malicious backlinks containing inappropriate content that may affect the reputation of official government domains. The system conducts regular scans, analyzes the results, and generates detailed reports to help security teams identify and mitigate these issues.

## Features
- Automated crawling of search engines to detect backlinks targeting government domains
- Random keyword generation focused on potentially malicious or inappropriate content
- Detailed analysis of detected backlinks with status checking
- Identification of attack vectors (Upload Forms, Redirect Backlinks, etc.)
- Automated report generation with domain statistics
- Scheduled execution with configurable intervals
- Telegram integration for notifications and report delivery

## Project Structure
```
his-soc-backlink/
├── step1.py - Initial search and domain extraction
├── step2.py - Detailed search for URLs on discovered domains
├── step3.py - URL verification and attack vector identification
├── step4.py - Excel formatting for daily reports
├── step5.py - Telegram notification for daily results
├── step6.py - Weekly report generation and aggregation
├── schedule.sh - Orchestration script for all steps
├── Dockerfile - Container configuration
├── crontab.txt - Scheduled execution configuration
├── setup.sh - Initial setup script
├── entrypoint.sh - Container entry point
├── data/ - Directory for storing collected data organized by month
├── logs/ - Directory for log files
├── archived/ - Directory for old versions of scripts
├── test/ - Test scripts and tools
└── various data files (.xlsx, .pkl, etc.)
```

## Workflow
1. **Keyword Generation (step1.py)**: Randomly selects potentially malicious keywords and creates search queries targeting government domains
2. **Domain Discovery (step1.py)**: Executes search queries to identify domains containing the keywords
3. **URL Extraction (step2.py)**: Extracts specific URLs from discovered domains
4. **Analysis (step3.py)**: Verifies each URL, checks its status, and identifies attack vectors
5. **Reporting (step4.py, step5.py)**: Formats results into readable reports and sends daily notifications
6. **Weekly Aggregation (step6.py)**: Generates comprehensive weekly reports every Friday evening

## Setup and Installation

### Prerequisites
- Python 3.7+
- Docker (for containerized deployment)
- Chrome/Chromium browser

### Required Python Packages
- selenium
- requests
- pandas
- openpyxl
- fake_useragent

### Docker Deployment
1. Build the base image:
```bash
docker build -t his-backlink:v1 .
```

2. Deploy the container:
```bash
docker run -d --name backlink-monitor his-backlink:v1
```

### Manual Setup
1. Clone the repository
2. Install the required dependencies:
```bash
pip install selenium requests pandas openpyxl fake_useragent
```
3. Run the setup script:
```bash
bash setup.sh
```
4. Configure the cron jobs:
```bash
crontab crontab.txt
```

## Configuration
- **Keywords**: Customize the target keywords in step1.py
- **Schedule**: Adjust the monitoring frequency in crontab.txt
- **Telegram**: Update the bot token and chat ID in step5.py for notifications

## Reports
- **Daily Reports**: Generated after each scan with details of newly discovered backlinks
- **Weekly Reports**: Comprehensive reports generated every Friday evening with statistics and trends

## Contributors
- HIS SOC Team

## License
Proprietary - All rights reserved 