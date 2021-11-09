import datetime
from flask import Flask, render_template, request
import logging
import os
from typing import Union
from google.cloud import storage

app = Flask(__name__, template_folder="templates")

# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
  #  dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
  #                 datetime.datetime(2018, 1, 2, 10, 30, 0),
  #                 datetime.datetime(2018, 1, 3, 11, 0, 0),
  #                 ]

    return render_template('root.html')

@app.route('/hiddenpage')
def rootSQRD():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
 #   dummy_times = [datetime.datetime(2000, 5, 25, 10, 0, 0),
 #                  datetime.datetime(2000, 5, 25, 10, 30, 0),
 #                  datetime.datetime(2000, 5, 25, 11, 0, 0),
  #                 ]

    return render_template('root.html')

@app.route('/upload-package')
def uploadPackage():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
 #   dummy_times = [datetime.datetime(2000, 5, 25, 10, 0, 0),
 #                  datetime.datetime(2000, 5, 25, 10, 30, 0),
 #                  datetime.datetime(2000, 5, 25, 11, 0, 0),
  #                 ]

    return render_template('upload_package.html')

@app.route('/retrieve-package')
def retrievePackage():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
 #   dummy_times = [datetime.datetime(2000, 5, 25, 10, 0, 0),
 #                  datetime.datetime(2000, 5, 25, 10, 30, 0),
 #                  datetime.datetime(2000, 5, 25, 11, 0, 0),
  #                 ]

    return render_template('retrieve_package.html')


@app.route('/upload', methods=['POST'])
def upload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    uploaded_file = request.files.get('file')

    if not uploaded_file:
        return 'No file uploaded.', 400

    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

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
    return render_template('upload_package_success.html')


@app.errorhandler(500)
def server_error(e: Union[Exception, int]) -> str:
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)