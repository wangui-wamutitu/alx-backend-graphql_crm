#!/usr/bin/env python3
"""
crm/tasks.py
Defines cron job helpers for the CRM app.
"""

from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from celery import shared_task

LOG_FILE = "/tmp/crm_report_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"


@shared_task
def generate_crm_report():
    try:
        transport = RequestsHTTPTransport(
            url=GRAPHQL_ENDPOINT,
            verify=True,
            retries=3,
        )

        client = Client(transport=transport, fetch_schema_from_transport=False)

        query = gql(
            """
            query {
                allCustomers {
                    id
                }
                allOrders {
                    id
                    totalAmount
                }
            }
            """
        )
        result = client.execute(query)
        
        total_customers = len(result["allCustomers"])
        total_orders = len(result["allOrders"])
        total_amount = sum(float(order["totalAmount"]) for order in result["allOrders"])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = (
            f"{timestamp} - Report: "
            f"{total_customers} customers, "
            f"{total_orders} orders, "
            f"{total_amount} revenue"
        )

        with open(LOG_FILE, "a") as f:
            f.write(message + "\n")

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = f"{timestamp} - Error generating CRM report: {e}"
        with open(LOG_FILE, "a") as f:
            f.write(error_msg + "\n")
