# 代码生成时间: 2025-09-04 20:06:41
# process_manager.py
# This script uses the Bottle framework to create a simple process manager.

from bottle import route, run, request, response
import subprocess
import os
import sys

# Define the base URL for our application
BASE_URL = '/process_manager'

# Home page that lists all running processes
@route(f"{BASE_URL}/")
def list_processes():
    # Retrieve the list of running processes
    try:
        processes = subprocess.check_output(['ps', '-ef']).decode('utf-8')
        return f"<pre>{processes}</pre>"
    except Exception as e:
        return f"Error: {e}", 500

# Route to start a new process
@route(f"{BASE_URL}/start", method='POST')
def start_process():
    command = request.forms.get('command')
    if not command:
        return {"error": "No command provided"}, 400
    try:
        # Start the process and get its PID
        process = subprocess.Popen(command, shell=True)
        return {"pid": process.pid, "message": "Process started"}
    except Exception as e:
        return f"Error starting process: {e}", 500

# Route to stop a process by its PID
@route(f"{BASE_URL}/stop", method='POST')
def stop_process():
    pid = request.forms.get('pid')
    if not pid:
        return {"error": "No process ID provided"}, 400
    try:
        os.kill(int(pid), 9)  # Send SIGKILL signal
        return {"pid": pid, "message": "Process stopped"}
    except Exception as e:
        return f"Error stopping process: {e}", 500

# Route to restart a process by its PID
@route(f"{BASE_URL}/restart", method='POST')
def restart_process():
    pid = request.forms.get('pid')
    command = request.forms.get('command')
    if not pid or not command:
        return {"error": "No process ID or command provided"}, 400
    try:
        # Stop the existing process
        os.kill(int(pid), 9)
        # Start a new process with the provided command
        process = subprocess.Popen(command, shell=True)
        return {"pid": process.pid, "message": "Process restarted"}
    except Exception as e:
        return f"Error restarting process: {e}", 500

# Run the Bottle application
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)