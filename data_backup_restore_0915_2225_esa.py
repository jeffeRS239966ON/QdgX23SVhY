# 代码生成时间: 2025-09-15 22:25:01
# data_backup_restore.py
# This script uses the Bottle framework to create a simple web service for data backup and restore.

import os
import json
import shutil
from bottle import route, run, request, response

# Define constants for data storage and backup
DATA_FOLDER = './data'
BACKUP_FOLDER = './backups'

# Ensure data and backup folders exist
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)

# Helper function to save data
def save_data(data):
    """Saves data to a file in JSON format."""
    filename = os.path.join(DATA_FOLDER, 'data.json')
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Helper function to load data
def load_data():
    """Loads data from a file in JSON format."""
    filename = os.path.join(DATA_FOLDER, 'data.json')
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Helper function to create a backup
def create_backup():
    """Creates a backup of the current data file."""
    src = os.path.join(DATA_FOLDER, 'data.json')
    dst = os.path.join(BACKUP_FOLDER, f'backup_{os.path.getmtime(src)}.json')
    shutil.copy2(src, dst)
    return dst

# Helper function to restore from a backup
def restore_backup(backup_file):
    """Restores data from a backup file."""
    src = backup_file
    dst = os.path.join(DATA_FOLDER, 'data.json')
    shutil.copy2(src, dst)
    return load_data()

# API endpoint for backing up data
@route('/backup', method='GET')
def backup_data():
    """Creates a backup of the current data and returns the backup file path."""
    try:
        backup_file = create_backup()
        return {'message': 'Backup successful', 'backup_file': backup_file}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# API endpoint for restoring data from a backup
@route('/restore', method='POST')
def restore_data():
    """Restores data from a provided backup file."""
    try:
        backup_file = request.json.get('backup_file')
        if not backup_file:
            response.status = 400
            return {'error': 'No backup file provided'}
        data = restore_backup(backup_file)
        return {'message': 'Restore successful', 'data': data}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# API endpoint for saving data
@route('/data', method='PUT')
def save_data_api():
    """Saves the provided data to the data file."""
    try:
        data = request.json.get('data')
        if not data:
            response.status = 400
            return {'error': 'No data provided'}
        save_data(data)
        return {'message': 'Data saved successfully'}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# API endpoint for loading data
@route('/data', method='GET')
def load_data_api():
    """Loads and returns the current data."""
    try:
        data = load_data()
        return {'data': data}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# Run the web service
if __name__ == '__main__':
    run(host='localhost', port=8080)