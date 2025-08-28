# 代码生成时间: 2025-08-28 23:50:17
#!/usr/bin/env python

"""
Process Manager using the Bottle framework.
This application allows users to manage system processes via HTTP requests.
"""

from bottle import route, run, request, response
import subprocess
import json
import sys

# Define the base URL for the process manager
BASE_URL = '/process_manager'

# Function to start a process
def start_process(command):
    """
    Start a new process using the given command.
    Args:
        command (str): The command to execute.
    Returns:
        str: The process ID of the started process.
    """
    try:
        process = subprocess.Popen(command, shell=True)
        return str(process.pid)
    except Exception as e:
        return str(e)

# Function to stop a process
def stop_process(process_id):
    """
    Stop a process by its process ID.
    Args:
        process_id (str): The process ID to stop.
    Returns:
        bool: True if the process was stopped successfully, False otherwise.
    """
    try:
        subprocess.call(['kill', '-9', str(process_id)], shell=True)
        return True
    except Exception as e:
        return str(e)

# Function to list all running processes
def list_processes():
    """
    List all running processes.
    Returns:
        list: A list of dictionaries containing process information.
    """
    try:
        processes = subprocess.check_output(['ps', 'aux']).decode('utf-8').split('
')
        return [{'process_id': line.split()[1], 'command': line.split()[10]} for line in processes[1:]]
    except Exception as e:
        return str(e)

# Route to start a new process
@route(f'{BASE_URL}/start', method='POST')
def start_process_route():
    """
    Handle POST requests to start a new process.
    """
    try:
        command = request.json['command']
        process_id = start_process(command)
        response.status = 200
        return json.dumps({'message': 'Process started successfully', 'process_id': process_id})
    except KeyError:
        response.status = 400
        return json.dumps({'error': 'Missing command parameter'})
    except Exception as e:
        response.status = 500
        return json.dumps({'error': str(e)})

# Route to stop a process
@route(f'{BASE_URL}/stop', method='POST')
def stop_process_route():
    """
    Handle POST requests to stop a process.
    """
    try:
        process_id = request.json['process_id']
        success = stop_process(process_id)
        response.status = 200
        return json.dumps({'message': 'Process stopped successfully' if success else 'Failed to stop process'})
    except KeyError:
        response.status = 400
        return json.dumps({'error': 'Missing process_id parameter'})
    except Exception as e:
        response.status = 500
        return json.dumps({'error': str(e)})

# Route to list all processes
@route(f'{BASE_URL}/list', method='GET')
def list_processes_route():
    """
    Handle GET requests to list all processes.
    """
    try:
        processes = list_processes()
        response.status = 200
        return json.dumps(processes)
    except Exception as e:
        response.status = 500
        return json.dumps({'error': str(e)})

# Run the Bottle application
if __name__ == '__main__':
    run(host='localhost', port=8080)