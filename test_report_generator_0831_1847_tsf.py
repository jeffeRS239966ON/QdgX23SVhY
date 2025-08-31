# 代码生成时间: 2025-08-31 18:47:30
# -*- coding: utf-8 -*-

"""
Test Report Generator using the Bottle framework.
This application generates test reports.
"""

from bottle import route, run, request, response, template
import json
import os

# Define the path for storing test reports
REPORTS_DIR = './test_reports'
os.makedirs(REPORTS_DIR, exist_ok=True)

# Define the route for generating a test report
@route('/report', method='POST')
def generate_report():
    # Get the JSON data from the request
    try:
        data = request.json
    except ValueError as e:
        # If the data is not in JSON format, return an error
        response.status = 400
        return json.dumps({'error': 'Invalid JSON data', 'message': str(e)})

    # Check if the required fields are present in the data
    required_fields = ['test_name', 'test_date', 'results']
    if not all(field in data for field in required_fields):
        response.status = 400
        return json.dumps({'error': 'Missing required fields'})

    # Generate the report file name
    report_name = f"{data['test_name']}_{data['test_date']}.json"
    report_path = os.path.join(REPORTS_DIR, report_name)

    # Write the report data to a file
    try:
        with open(report_path, 'w') as report_file:
            json.dump(data, report_file)
    except Exception as e:
        response.status = 500
        return json.dumps({'error': 'Failed to write report', 'message': str(e)})

    # Return the success message with the report path
    return json.dumps({'message': 'Report generated successfully', 'report_path': report_path})

# Start the Bottle application
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)