# 代码生成时间: 2025-08-25 16:14:16
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A simple Bottle-based application to convert documents.
"""

from bottle import route, run, request, response, static_file
import os
import mimetypes

# Define the directory where static files (like CSS, JS) are located
STATIC_DIR = 'static'

# Define the directory where uploaded files will be temporarily stored
UPLOAD_DIR = 'uploads'

# Define the allowed file extensions for conversion
ALLOWED_EXTENSIONS = {'doc', 'docx', 'odt', 'pdf', 'txt'}


def allowed_file(filename, extensions=ALLOWED_EXTENSIONS):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@route('/upload', method='POST')
def upload_file():
    """Upload a file and return a JSON response."""
    try:
        # Check if the request has the file part
        if 'file' not in request.files:
            return {'error': 'No file part'}

        file = request.files['file']

        # Check if the file is allowed
        if file.filename == '' or not allowed_file(file.filename):
            return {'error': 'File type not allowed'}

        # Save the file to the upload directory
        filepath = os.path.join(UPLOAD_DIR, file.filename)
        file.save(filepath)

        # Return a success message
        return {'message': 'File uploaded successfully', 'filename': file.filename}
    except Exception as e:
        # Return an error message with the exception details
        return {'error': str(e)}

@route('/static/<filename:path>')
def send_static(filename):
    """Serve static files like CSS and JS."""
    return static_file(filename, root=STATIC_DIR)

@route('/download/<filename:path>')
def download_file(filename):
    """Download the converted file."""
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        return {'error': 'File not found'}

    response.content_type = mimetypes.guess_type(filename)[0]
    return static_file(filename, root=UPLOAD_DIR)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
