#!/usr/bin/env python3
"""
crm/cron.py
Defines cron job helpers for the CRM app.
"""

from datetime import datetime
import requests

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"


def log_crm_heartbeat():
    """
    Logs a heartbeat message to confirm CRM cron is alive.
    Format: DD/MM/YYYY-HH:MM:SS CRM is alive
    Optionally queries the GraphQL 'hello' field to verify endpoint responsiveness.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # Verify GraphQL endpoint
    try:
        query = {"query": "{ hello }"}
        response = requests.post(GRAPHQL_ENDPOINT, json=query, timeout=5)
        if response.ok:
            data = response.json()
            hello_value = data.get("data", {}).get("hello")
            if hello_value:
                message += f" | GraphQL hello: {hello_value}"
            else:
                message += " | GraphQL responded but no hello field"
        else:
            message += f" | GraphQL error: HTTP {response.status_code}"
    except Exception as e:
        message += f" | GraphQL check failed: {e}"

    # Append to log file
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

