# 代码生成时间: 2025-08-11 09:54:15
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
System Performance Monitor

A simple Bottle web application to monitor system performance.
"""

from bottle import route, run, template, static_file
import psutil
import os
import json

# Define the root path for static files
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# Define the port and host for the Bottle server
HOST = 'localhost'
PORT = 8080


# Home page route
@route('/')
def index():
    return static_file('index.html', root=STATIC_ROOT)

# System performance route
@route('/performance')
def system_performance():
    try:
        # Get system performance metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        # Create a dictionary with the performance metrics
        performance_data = {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage
        }
        
        # Return the performance data as JSON
        return json.dumps(performance_data)
    
    except Exception as e:
        # Handle any exceptions and return an error message
        return json.dumps({'error': str(e)})

# Run the Bottle server
if __name__ == '__main__':
    run(host=HOST, port=PORT)
