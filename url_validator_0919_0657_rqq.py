# 代码生成时间: 2025-09-19 06:57:46
# url_validator.py

# Import necessary modules
# 增强安全性
from bottle import route, run, request, HTTPError
import requests
import urllib.parse
# 改进用户体验

# Define a function to validate a URL
def is_valid_url(url):
    # Parse the URL to ensure it's properly formatted
    parsed_url = urllib.parse.urlparse(url)
    # Check if the scheme and netloc are present
# TODO: 优化性能
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return False
    return True

# Define a Bottle route for validating a URL
@route('/validate_url', method='GET')
def validate_url():
    # Get the URL from the query parameters
    url_to_validate = request.query.url
    
    # Check if the URL is provided
    if not url_to_validate:
        raise HTTPError(400, 'URL parameter is missing')
    
    # Validate the URL
    if is_valid_url(url_to_validate):
        # Try to make a HEAD request to the URL to check if it's reachable
        try:
            response = requests.head(url_to_validate, allow_redirects=True, timeout=5)
            # If the URL is reachable and has a 2xx status code, it's valid
            if response.status_code // 100 == 2:
                return {"valid": True, "message": "The URL is valid"}
            else:
                return {"valid": False, "message": "There was a problem accessing the URL"}
        except requests.RequestException as e:
            # If there's a network-related error, the URL is not considered valid
            return {"valid": False, "message": str(e)}
    else:
        # If the URL is not properly formatted, it's invalid
        return {"valid": False, "message": "The URL is not properly formatted"}

# Run the Bottle application
if __name__ == '__main__':
    run(host='localhost', port=8080)
# NOTE: 重要实现细节