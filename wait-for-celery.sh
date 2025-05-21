#!/bin/bash


echo "Waiting for Celery workers to be ready..."

# چک کردن اینکه آیا Workerها به Redis وصل شدن و آماده‌ان
until celery -A roshan_news inspect ping; do
    echo "Celery workers not ready yet, waiting..."
    sleep 5
done

echo "Celery workers are ready!"

# اجرای دستور Flower
exec "$@"