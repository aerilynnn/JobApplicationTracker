#!/bin/bash
set -euo pipefail

echo "Creating S3 bucket..."
awslocal s3 mb s3://job-tracker-documents

echo "Creating SQS queues..."
awslocal sqs create-queue --queue-name job-tracker-scrape-dlq
awslocal sqs create-queue --queue-name job-tracker-scrape

echo "LocalStack resources ready."
