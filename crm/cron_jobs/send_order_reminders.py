#!/usr/bin/env python3
"""
send_order_reminders.py
Queries recent orders via GraphQL and logs order IDs + customer emails.
"""

import sys
from datetime import datetime, timedelta, timezone
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

def main():
    transport = RequestsHTTPTransport(
        url=GRAPHQL_ENDPOINT,
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query to fetch all orders
    query = gql(
        """
        query GetOrders {
          orders {
            id
            orderDate
            customer {
              email
            }
          }
        }
        """
    )

    try:
        result = client.execute(query)
        orders = result.get("orders", [])
    except Exception as e:
        print(f"Error querying GraphQL: {e}", file=sys.stderr)
        sys.exit(1)

    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

    # Filter orders
    recent_orders = []
    for order in orders:
        order_date_str = order.get("orderDate")
        try:
            order_date = datetime.fromisoformat(order_date_str.replace("Z", "+00:00"))
            if order_date >= seven_days_ago:
                recent_orders.append(order)
        except Exception:
            continue

    # Log results
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    with open(LOG_FILE, "a") as f:
        for order in recent_orders:
            order_id = order.get("id")
            email = order.get("customer", {}).get("email")
            if order_id and email:
                f.write(f"[{timestamp}] Order ID: {order_id}, Customer Email: {email}\n")

    print("Order reminders processed!")

if __name__ == "__main__":
    main()
