import datetime
import subprocess
import sys
import json
import flask as fk
from flask.globals import request
import flask_restful as fkr
import logging
import os
from io import BytesIO
from typing import Union
from flask.helpers import url_for
from google.cloud import storage
from google.cloud.storage import client
from werkzeug.utils import redirect, secure_filename
import pymysql
import json
import main
import base64




@main.app.route('/api/upload2', methods=['POST'])
def APIupload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(main.CLOUD_STORAGE_BUCKET)

    if fk.request.method == 'POST':
        # check if the post request has the file part
        if 'files' not in fk.request.files:
            
            return fk.redirect(fk.request.url)
        uploaded_files = fk.request.files.getlist('files')



    
    
    
    for uploaded_file in uploaded_files:
        
        if not (uploaded_file):
            return 'No file uploaded.', 400
        if not (main.allowed_file(uploaded_file.filename)):
            return 'Unallowed file type uploaded. Only .zip files are accepted at this time.', 400            
        if uploaded_file.filename == '':
            return 'No selected file', 400 

        uploaded_file.name = secure_filename(uploaded_file.name)   #ensure the filename is OK for computers
        if uploaded_file.filename == '':
            return 'secure_filename broke and returned an empty filename', 400 


        #Upload rate information SQL Database
        conn = main.connecttoDB()
        cursor = conn.cursor()
        data = main.parseJson("output.json")
        try:
            for entry in data["scores"]:
                cursor.execute("INSERT INTO scores_table (url, ramp_up_score, correctness_score, bus_factor_score, responsive_maintainer_score, license_score, dependency_score) VALUES(%s, %s, %s, %s, %s, %s, %s)", (entry["url"], entry["rampup"], entry["correctness"], entry["busfactor"], entry["contributors"], entry["license"], entry["dependency"]))

            conn.commit()
            pass
        except:
            pass


        # Create a new blob and upload the file's content.
        blob = bucket.blob(uploaded_file.filename)

        blob.upload_from_string(
            uploaded_file.read(),
            content_type=uploaded_file.content_type
        )

    # Make the blob public. This is not necessary if the
    # entire bucket is public.
    # See https://cloud.google.com/storage/docs/access-control/making-data-public.
    #blob.make_public()

    # The public URL can be used to directly access the uploaded file via HTTP.
    #return blob.public_url
    return fk.render_template('upload_package_success.html')