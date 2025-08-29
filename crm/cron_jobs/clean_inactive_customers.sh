#!/bin/bash
# clean_inactive_customers.sh
# Deletes customers with no orders in the past year and logs the results.

# Go to project root (adjust if needed)
cd "$(dirname "$0")/../.." || exit 1

# Run Django shell command
DELETED_COUNT=$(python manage.py shell -c "
import datetime
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - datetime.timedelta(days=365)
inactive_customers = Customer.objects.exclude(
    order__order_date__gte=one_year_ago
)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log with timestamp
echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] Deleted \$DELETED_COUNT inactive customers\" >> /tmp/customer_cleanup_log.txt
