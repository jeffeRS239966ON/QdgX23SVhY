# 代码生成时间: 2025-09-13 16:12:02
from bottle import route, run, request, response
from PIL import Image
import os
import io
import sys

"""Batch Image Resizer Web Service

This Bottle web application allows users to upload multiple images and specify a target size.
It then resizes each image while maintaining the aspect ratio and returns the resized images."""

# Define the target size for resizing images
TARGET_SIZE = (800, 800)

# Define the route for uploading images and specifying target size
@route('/resize', method='POST')
def resize_images():
    # Get the uploaded files from the request
    uploaded_files = request.files
    # Get the target size from the form data
    target_size = request.forms.get('size').split('x')
    # Convert the target size to integers
    target_size = (int(target_size[0]), int(target_size[1]))

    if not uploaded_files:
        return {"error": "No files uploaded"}

    resized_images = []
    for file in uploaded_files.values():
        try:
            # Open the uploaded image file
            with Image.open(file.file) as img:
                # Resize the image while maintaining the aspect ratio
                img.thumbnail(target_size, Image.ANTIALIAS)
                # Save the resized image to a bytes buffer
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG')
                buffer.seek(0)
                # Append the resized image buffer to the list
                resized_images.append(buffer)
        except IOError:
            # Handle any IO errors that occur
            return {"error": f"Failed to process {file.filename}"}

    # Set the response header to indicate that we are sending images
    response.content_type = 'multipart/x-mixed-replace; boundary=--boundary'
    
    # Yield each resized image with the appropriate headers
    for i, buffer in enumerate(resized_images):
        yield '--boundary'
        yield 'Content-Type: image/jpeg'
        yield 'Content-Length: %d' % len(buffer.getvalue())
        yield ''
        yield buffer.getvalue()
        buffer.close()
    yield '--boundary--'
    return

# Start the Bottle web server
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)