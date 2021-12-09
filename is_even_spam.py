import datetime
import subprocess
import sys
import json
import logging
import os
import json
import base64
import zipfile
from io import BytesIO
from typing import Union
from flask.helpers import url_for
from google.cloud import storage
from google.cloud.storage import client
from werkzeug.utils import redirect, secure_filename
from google.cloud import secretmanager


CLOUD_STORAGE_BUCKET = 'package_storage'
gcs = storage.Client()
bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
is_even_ID = 7946
is_even_zip = open("is-even_package3_0.1.2.zip", "rb")
while is_even_ID < 50000:
    final_file_name = 'is-even_ID' + str(is_even_ID) + '_0.1.2.zip'
    blob = bucket.blob(final_file_name)
    blob.upload_from_string(is_even_zip.read(), content_type='application/zip')
    is_even_zip.seek(0)
    print("Uploaded ", is_even_ID+1, " packages. All hail John Schlinkert.")
    is_even_ID += 1
