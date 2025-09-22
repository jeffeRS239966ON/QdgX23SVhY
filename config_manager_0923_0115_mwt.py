# 代码生成时间: 2025-09-23 01:15:26
# config_manager.py

"""
A Bottle-based application to manage configuration files.
This application allows users to load and save configuration files.
"""

from bottle import route, run, request, response, static_file
import json
import os

# Define the directory where configuration files are stored
CONFIG_DIR = 'configs/'

# Ensure the configuration directory exists
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# Route to load a configuration file
@route('/config/<filename:path>')
def load_config(filename):
    """
    Load a configuration file and return its content.
    :param filename: The name of the configuration file to load.
    :return: The content of the configuration file as JSON.
    """
    try:
        with open(os.path.join(CONFIG_DIR, filename), 'r') as file:
            config = json.load(file)
            return json.dumps(config)
    except FileNotFoundError:
        response.status = 404
        return json.dumps({'error': 'Configuration file not found'})
    except json.JSONDecodeError:
        response.status = 500
        return json.dumps({'error': 'Invalid configuration file format'})

# Route to save a configuration file
@route('/config/<filename:path>', method='POST')
def save_config(filename):
    """
    Save a configuration file.
    :param filename: The name of the configuration file to save.
    :return: A success message if the file is saved, otherwise an error message.
    """
    try:
        config = request.json
        with open(os.path.join(CONFIG_DIR, filename), 'w') as file:
            json.dump(config, file)
        return json.dumps({'message': 'Configuration file saved successfully'})
    except TypeError:
        response.status = 400
        return json.dumps({'error': 'Invalid JSON data provided'})
    except IOError:
        response.status = 500
        return json.dumps({'error': 'Failed to save configuration file'})

# Run the application
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
