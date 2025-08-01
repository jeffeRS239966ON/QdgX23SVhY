# 代码生成时间: 2025-08-02 06:06:59
# -*- coding: utf-8 -*-

"""
File Backup and Sync Tool using Python and Bottle framework.
This script provides a simple web interface for file backup and synchronization.
"""

from bottle import Bottle, run, route, request, response, static_file
import os
import shutil
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Bottle()

# Define the source and destination directories
SOURCE_DIR = "/source/directory"
DESTINATION_DIR = "/destination/directory"

# Check if directories exist and create if not
if not os.path.exists(SOURCE_DIR):
    os.makedirs(SOURCE_DIR)
if not os.path.exists(DESTINATION_DIR):
    os.makedirs(DESTINATION_DIR)

# Route for serving static files
@app.route("/static/<filename:path>")
def serve_static(filename):
    return static_file(filename, root="./static")

# Route for backing up files
@app.route("/backup", method="POST")
def backup_files():
    """
    Back up files from the source directory to the destination directory.
    Returns a JSON response indicating success or failure.
    """
    try:
        for file_name in os.listdir(SOURCE_DIR):
            file_path = os.path.join(SOURCE_DIR, file_name)
            dest_path = os.path.join(DESTINATION_DIR, file_name)
            if os.path.isfile(file_path):
                shutil.copy2(file_path, dest_path)
        response.status = 200
        return {"message": "Backup successful"}
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        response.status = 500
        return {"error": str(e)}

# Route for synchronizing files
@app.route("/sync", method="POST")
def sync_files():
    """
    Synchronize files between the source and destination directories.
    Returns a JSON response indicating success or failure.
    """
    try:
        # Check for new files in source directory and copy them to the destination
        for file_name in os.listdir(SOURCE_DIR):
            file_path = os.path.join(SOURCE_DIR, file_name)
            dest_path = os.path.join(DESTINATION_DIR, file_name)
            if os.path.isfile(file_path) and not os.path.exists(dest_path):
                shutil.copy2(file_path, dest_path)
        # Check for deleted files in source directory and remove them from the destination
        for file_name in os.listdir(DESTINATION_DIR):
            file_path = os.path.join(DESTINATION_DIR, file_name)
            source_path = os.path.join(SOURCE_DIR, file_name)
            if os.path.isfile(file_path) and not os.path.exists(source_path):
                os.remove(file_path)
        response.status = 200
        return {"message": "Synchronization successful"}
    except Exception as e:
        logger.error(f"Synchronization failed: {e}")
        response.status = 500
        return {"error": str(e)}

if __name__ == "__main__":
    # Start the Bottle server
    run(app, host="localhost", port=8080)
