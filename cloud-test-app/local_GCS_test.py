import datetime
from flask import Flask, render_template, request
import logging
import os
from typing import Union
from google.cloud import storage
from google.cloud.storage import client

MAX_RESULTS_PER_PAGE = 10
# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

def round_up(dividend, divisor) -> int:
    output = int(dividend // divisor + (dividend % divisor > 0))
    return output

gcs = storage.Client()

# Get the bucket that the file will be uploaded to.
bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

blob_iter = bucket.list_blobs(bucket)
curr_page = 10
all_pages = bucket.list_blobs().pages
total_blobs = 0
for page in all_pages:
    total_blobs += page.num_items
max_pages = round_up(total_blobs, MAX_RESULTS_PER_PAGE)
max_results = MAX_RESULTS_PER_PAGE * curr_page
for  index_blobs, blob in enumerate(bucket.list_blobs(max_results=max_results)):
    if index_blobs >= ((curr_page-1) * MAX_RESULTS_PER_PAGE):
        print("Blob index is: ",index_blobs, " with name ", blob.name, " on page ", page)

#for  index_pages, page in enumerate(bucket.list_blobs().pages):
#    for index_blob,blob in enumerate(page):
#        print("At index: ",index_blob, " IS BLOB: ",blob.name)
#    print("PAGE Index is: ",index_pages, " with page ", page.num_items)

gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
#blobs = []
blobs = [blob_new.name for blob_new in bucket.list_blobs()]
#for blob_new in bucket.list_blobs():
#    blobs.append(blob_new.name)

print("\n",blobs)
