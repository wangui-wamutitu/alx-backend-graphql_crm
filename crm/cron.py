#!/usr/bin/env python3
"""
crm/cron.py
Defines cron job helpers for the CRM app.
"""

from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
LOG_LOW_PROD_FILE = '/tmp/low_stock_updates_log.txt'
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"


def log_crm_heartbeat():
    """
    Logs a heartbeat message to confirm CRM cron is alive.
    Format: DD/MM/YYYY-HH:MM:SS CRM is alive
    Optionally queries the GraphQL 'hello' field to verify endpoint responsiveness.
    """
    # Current timestamp
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    try:
        transport = RequestsHTTPTransport(
            url=GRAPHQL_ENDPOINT,
            verify=True,
            retries=3,
        )

        client = Client(transport=transport, fetch_schema_from_transport=False)

        query = gql("{ hello }")
        result = client.execute(query)

        hello_value = result.get("hello")
        if hello_value:
            message += f" | GraphQL hello: {hello_value}"
        else:
            message += " | GraphQL responded but no hello field"
    except Exception as e:
        message += f" | GraphQL check failed: {e}"

    # Append log
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")


def update_low_stock():
    try:
        transport = RequestsHTTPTransport(
            url=GRAPHQL_ENDPOINT,
            verify=True,
            retries=3,
        )

        client = Client(transport=transport, fetch_schema_from_transport=False)

        mutation = gql(
            """
            mutation {
                updateLowStockProducts {
                    success
                    message
                    updatedProducts {
                    id
                    name
                    price
                    stock
                    }
                }
            }
            """
        )
        result = client.execute(mutation)
        data = result.get("updateLowStockProducts", {})
        timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

        with open(LOG_LOW_PROD_FILE, "a") as f:
            for product in data.get("updatedProducts", []):
                log_message = f"{timestamp}: {product['name']} has {product['stock']} in stock"
                f.write(log_message + "\n")

    except Exception as e:
        timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        error_message = f"{timestamp}: An error occurred in update_low_stock - {e}"
        with open(LOG_LOW_PROD_FILE, "a") as f:
            f.write(error_message + "\n")
