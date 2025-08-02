# 代码生成时间: 2025-08-03 06:28:27
#!/usr/bin/env python

# image_resizer.py
# This script is a Bottle-based web service that allows users to batch adjust image sizes.

import os
from bottle import route, run, request, response, static_file
from PIL import Image

# Define the root directory for the uploaded images
UPLOAD_DIR = 'uploaded_images/'

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Define the route for serving static files (uploaded images)
@route('/static/<filepath:path>')
# FIXME: 处理边界情况
def server_static(filepath):
    return static_file(filepath, root=UPLOAD_DIR)
# 添加错误处理

# Define the route for uploading images
# 优化算法效率
@route('/upload', method='POST')
# FIXME: 处理边界情况
def upload():
# 增强安全性
    """
    Handle the image upload, resize the image and save it.
# 改进用户体验
    """
    try:
        # Check if file is uploaded
        if not request.files:
            response.status = 400
            return {'error': 'No file uploaded.'}

        # Get the uploaded file
        image_file = request.files['image']

        # Generate a unique file name for the uploaded image
        filename = UPLOAD_DIR + image_file.filename.replace(' ','_')

        # Save the uploaded image
        with open(filename, 'wb') as f:
# TODO: 优化性能
            f.write(image_file.file.read())

        # Define the size to which the image will be resized
        target_size = (800, 600)

        # Open and resize the image
        image = Image.open(filename)
        image = image.resize(target_size)

        # Save the resized image with a new name (appending '_resized')
        resized_filename = filename.rsplit('.', 1)[0] + '_resized.' + filename.rsplit('.', 1)[1]
# 添加错误处理
        image.save(resized_filename)

        # Return the path to the resized image for display
        return {'resized_path': '/static/' + os.path.basename(resized_filename)}

    except Exception as e:
        # Handle exceptions and return error messages
        response.status = 500
        return {'error': str(e)}
# 增强安全性

# Start the Bottle server on localhost port 8080
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)