import datetime
import subprocess
import sys
import json
import flask as fk
import logging
import os
from io import BytesIO
from typing import Union
from google.cloud import storage
from google.cloud.storage import client
from werkzeug.utils import secure_filename

app = fk.Flask(__name__, template_folder="templates")

# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
MAX_RESULTS_PER_PAGE = 10
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def round_up(dividend, divisor) -> int:
    output = int(dividend // divisor + (dividend % divisor > 0))
    return output

@app.route('/')
def root():


    return fk.render_template('root.html')

@app.route('/java-version')
def javaVersion():
    output2 = subprocess.run(["./Java_install/jdk-11.0.13/bin/java", "-jar", "Main.jar"], capture_output=True) # We want this to be a string that looks like json

    version2 = output2.stdout.decode("utf-8")
    version3 = output2.stderr.decode("utf-8")
    print(output2.stdout.decode("utf-8"))
    version1 = "java placeholder"
    version1 = sys.platform
    return fk.render_template('javaversion.html', java_version1 = version1, java_version2 = version2, java_version3 = version3)

@app.route('/hiddenpage')
def rootSQRD():


    return fk.render_template('root.html')

@app.route('/upload-package')
def uploadPackage():


    return fk.render_template('upload_package.html')


@app.route('/download-package', methods=['POST'])
def downloadPackage():
    if fk.request.method == 'POST':
        get_package_index = int(fk.request.form['package_index'])

    gcs = storage.Client()

    # Get the bucket that the file will be downloaded from.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blobs = [blob_new.name for blob_new in bucket.list_blobs()] # List all the blobs available
    target_name =  blobs[get_package_index] #Get the blob name
    target_blob = bucket.blob(target_name)  #Get the right blob by filename
    print(target_blob)
    print(type(target_blob))
    #file_to_download = target_blob.download_to_filename(target_name)
    #print("file_to_download TYPE: ", type(file_to_download))
    bytes = target_blob.download_as_bytes()
    #bytes.seek(0,0)
    #print("FILE TYPE: ",type(file_to_download))
    print("BYTES TYPE: ",type(bytes))
    #print("BYTES: \n\n",bytes)
    bytes_as_file = BytesIO(bytes)
    #URL_to_download = 'https://storage.googleapis.com/ece-461-project-2-team-4.appspot.com/' + target_name
    #print(URL_to_download)

    
    #return fk.render_template('download_package_success.html', URL_to_download=URL_to_download)
    #return fk.render_template('download_package_success.html')
    return fk.send_file(bytes_as_file, as_attachment=True, attachment_filename=target_name)

@app.route('/view-packages', methods=['GET', 'POST'])
def viewPackages(curr_page = 1):
    fk.render_template('loading.html')
    if fk.request.method == 'POST':
        curr_page = fk.request.form['next_page']
    print("CURR PAGE1: ", curr_page)
    try:
        curr_page = int(curr_page)
    except:
        curr_page = 1
    print("CURR PAGE2: ", curr_page)
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    #blob_iter = bucket.list_blobs(bucket)
    #curr_page = 1                          #hard coded placeholder

    all_pages = bucket.list_blobs().pages
    total_blobs = 0
    for page in all_pages:
        total_blobs += page.num_items
    max_pages = round_up(total_blobs, MAX_RESULTS_PER_PAGE)
    if (curr_page < 1):           #Should we deal with an upper bound?
        curr_page = 1
    elif(curr_page > max_pages):
        curr_page = max_pages
    max_results = MAX_RESULTS_PER_PAGE * curr_page
    package_identifiers = []
    print("CURR PAGE3: ", curr_page)
    for  index_blobs, blob in enumerate(bucket.list_blobs(max_results=max_results)):
        if index_blobs >= ((curr_page-1) * MAX_RESULTS_PER_PAGE):
            print("Blob index is: ",index_blobs, " with name ", blob.name, " on page ", page)
            blob_tuple = (index_blobs, blob.name)
            package_identifiers.append(blob_tuple)


    return fk.render_template('view_packages.html', package_identifiers=package_identifiers, curr_page=curr_page, max_pages=max_pages)

@app.route('/upload', methods=['POST'])
def upload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    if fk.request.method == 'POST':
        # check if the post request has the file part
        if 'files' not in fk.request.files:
            
            return fk.redirect(fk.request.url)
        uploaded_files = fk.request.files.getlist('files')


    
    
    
    for uploaded_file in uploaded_files:
        
        if not (uploaded_file):
            return 'No file uploaded.', 400
        if not (allowed_file(uploaded_file.filename)):
            return 'Unallowed file type uploaded.', 400            
        if uploaded_file.filename == '':
            return 'No selected file', 400 

        uploaded_file.name = secure_filename(uploaded_file.name)   #ensure the filename is OK for computers
        if uploaded_file.filename == '':
            return 'secure_filename broke and returned an empty filename', 400 


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