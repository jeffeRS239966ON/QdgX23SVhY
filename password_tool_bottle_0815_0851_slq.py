# 代码生成时间: 2025-08-15 08:51:20
from bottle import route, run, request, response
from cryptography.fernet import Fernet
import base64

# Generate a key for encryption and decryption
# This should be stored securely, not hardcoded
SECRET_KEY = base64.urlsafe_b64encode(b'your-secret-key')

# Initialize Fernet with the secret key
fernet = Fernet(SECRET_KEY)

# Define the route for password encryption
@route('encrypt', method='POST')
def encrypt_password():
    # Get the password from the request
    data = request.json
    password = data.get('password')

    # Check if password is provided
    if not password:
        response.status = 400
        return {"error": "Password is required"}

    try:
        # Encrypt the password
        encrypted_password = fernet.encrypt(password.encode()).decode()
        return {"encrypted": encrypted_password}
    except Exception as e:
        # Handle encryption errors
        response.status = 500
        return {"error": str(e)}

# Define the route for password decryption
@route('decrypt', method='POST')
def decrypt_password():
    # Get the encrypted password from the request
    data = request.json
    encrypted_password = data.get('encrypted')

    # Check if encrypted password is provided
    if not encrypted_password:
        response.status = 400
        return {"error": "Encrypted password is required"}

    try:
        # Decrypt the password
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        return {"decrypted": decrypted_password}
    except Exception as e:
        # Handle decryption errors
        response.status = 500
        return {"error": str(e)}

# Start the Bottle server
if __name__ == '__main__':
    run(host='localhost', port=8080)