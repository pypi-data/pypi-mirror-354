# 🖥️ Clockwerk (Uptime Monitor)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI - 0.1.0](https://img.shields.io/badge/PyPI-coming--soon-yellow)](https://pypi.org/)

---

Clockwerk is a Python application designed to monitor the availability and performance 
(latency or status) of various API Endpoints (URLs). It tracks the health of the monitored endpoint and stores the results in a database for future analysis and reporting. The application uses SQLalchemy's ORM-based database interaction to store results, and Asyncio's async sessions for asynchronous operations.

## 🚀 Key Features
* 🔍 Monitors multiple endpoints
* ⏱️ Tracks endpoint health and status with real-time status updates
* 📊 Logs the latency and status code for each request
* 🗃️ Stores monitoring results in a database of your own choice
* ⚡ Supports asynchronous database operations to ensure high performance
* 🚨 Sends alert message to report endpoint failure or latency
* 🧩 Supports MySQL, PostgreSQL and SQLite

## 📦 Installation
```bash
pip install clockwerk 
poetry add clockwerk


## 🌎 Code Usage
>> Start by creating the necessary config models `MonitorConfig`, `EmailConfig`, `DatabaseConfig`.

```python
# Import the necessary config-models and scheduling loop
from clockwerk.scheduler import scheduling_loop
from clockwerk.config import MonitorConfig, EmailConfig, DatabaseConfig
from clockwerk.models import Endpoint

# Create an instance of the MonitorConfig to specify monitored endpoints.
monitor_config = MonitorConfig(
    endpoints = [
        Endpoint(url: "https://test-exmaple.com", timeout=2, alert_threshold=3),
        Endpoint(url: "https://api_testpoint.org", timeout=3, alert_threshold=2)
    ], 
    check_interval = 60,        # Checks the specified endpoints every 60 seconds.
    latency_threshold = 1.5     # Raises an alert if the endpoint latency exceeds the specified number (seconds)
)

# Model for e-mail configuration used to raise and send alert messages.
email_config = EmailConfig(
    smtp_host="smtp.mailtrap.io",               # SMTP Host
    smtp_port=587,                              # Port to run your email alerts from
    email_from="randommail@yourdomain.com",     # Email address sending the alerts
    email_to="alerts@yourdomain.com"            # Email address receiving the alerts.
)

# Database configuration model (MySQL, PostgreSQL, SQLite)
db_config = DatabaseConfig(
    db_activation=True,             # Writes results to DB if True.
    db_driver="sqlite",             # Specify the desired DB platform.
    db_name="clockwerk.db",         # Identifying name for DB.
    db_user="root",                 # Identifying user for DB.
    db_password="SuperSecret123",   # Individual password for DB access.
    db_host="localhost",            # Host associated with current DB.
    db_port=1200                    # Available port to run DB connection on.
)

```

>> Utilise the config models to create an instance of `scheduling_loop` to run.
>> As Clockwerk's monitor is an async function it can be run with either `asyncio.run()` or `await`.

```python
# Import the necessary config-models and scheduling loop
import asyncio
from clockwerk.scheduler import scheduling_loop
from clockwerk.config import MonitorConfig, EmailConfig, DatabaseConfig
from clockwerk.models import Endpoint

# Run the scheduling loop (if running the loop from a synchronous context)
asyncio.run(scheduling_loop(
    monitor_config=monitor_config,
    email_config=email_config,
    db_config=db_config
))

# Run the scheduling loop (if running the loop from an asynchronous context)
await scheduling_loop(
    monitor_config=monitor_config,
    email_config=email_config,
    db_config=db_config
)

```

## 📋 Monitor & Endpoints
>> In order to properly configure the main scheduling_loop, Clockwerk requires a list of specified *endpoints* (URLs) scheduled for monitoring.
>> These *endpoints* are passed in to the main configuration object (MonitorConfig), along with specifications detailing the interval between checks and maximum latency allowed:
`check_interval`, `latency_threshold`.

| **Parameters**    | **Description**                                                   |
|-------------------|-------------------------------------------------------------------|
| endpoints         | A list of endpoint-objects to monitor.                            |
| check_interval    | Time in seconds between each health check (Default: 60)           |
| latency_threshold | Max latency in seconds before triggering an alert (Default: 1.0)  |

## ✉️ E-mail Alerts
>> Additionally, Clockwerk supports asynchronous email alerts (**aiohttp**) sent to individual e-mails if monitored Endpoints fail their respective health check.

| **Parameters** | **Description**                                                        |
|----------------|------------------------------------------------------------------------|
| smtp_host      | SMTP server for sending email alerts.                                  |
| smtp_port      | SMTP port (Default: 587)                                              |
| email_from     | Sender's e-mail address.                                               |
| email_to       | Recipient's e-mail address.                                            |

## ♾️ Database Setup
>> Clockwerk supports asynchronous database operations, allowing users to dynamically store results in one of three currently supported database platforms:
`MySQL`, `PostgreSQL`, `SQLite`
>> Built on SQLalchemy's asynchronous sessions and ORM framework, allowing for quick and seamless database connection and storage.
>> If the individual user **does not** require results stored in a database, simply set the DatabaseConfig's activation variable to False, `db_activation=False`. This disables any form of database connection used by the scheduling loop. 

```python
# To initialise database connectivity use a DatabaseConfig object to specify desired parameters.
from clockwerk.config import DatabaseConfig
```

| **Parameter** | **Description**                                                      |
|---------------|----------------------------------------------------------------------|
| db_activation | Enable/Disable database connection and storage (Default: False)      |
| db_driver     | One of available drivers `MySQL`, `PostgreSQL`, `SQLite`             |
| db_host       | Database host (e.g. localhost)                                       |
| db_name       | Identifying name of the target database                              |
| db_user       | Username for database connection                                     |
| db_password   | Password for database access                                         |
| db_port       | Port used to connect to database                                     |

## 📈 Future Roadmap

Roadmap over future improvements and application extensions.
* Slack / Webhook integration for alerts.
* Docker support for deployment
* Dashboard with data analysis and visualisation (*Prometheus*)

## 🤝 Contributing 

Contributions to the application's future improvements are more than welcome. Feel free to open an issue or submit a pull request.
1. Fork the repo
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -am "Add new feature"`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull request

## 📝 Licensing

This project is licensed under [MIT License](https://opensource.org/license/mit).
