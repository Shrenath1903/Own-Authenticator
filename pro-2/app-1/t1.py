from flask import Flask, jsonify, render_template
import secrets
import string
import time

app = Flask(__name__)

# Global variables to store the cached password and its generation time
cached_password = None
last_generated_time = None

def generate_random_string(length=10):
    """Generate a random alphanumeric string of the specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_password_for_current_minute():
    """Return a password that updates every minute."""
    global cached_password, last_generated_time
    current_time = int(time.time())  # Current time in seconds
    current_minute = current_time // 60  # Current minute
    
    if last_generated_time == current_minute and cached_password is not None:
        # Return the cached password if still in the same minute
        return cached_password
    
    # Generate a new password for the new minute
    cached_password = generate_random_string(10)
    last_generated_time = current_minute
    return cached_password

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML page

@app.route('/get_password', methods=['GET'])
def get_password():
    current_password = get_password_for_current_minute()  # Generate or retrieve password
    print(f"Generated password: {current_password}")  # Debugging
    return jsonify({'password': current_password})  # Return as JSON

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Run Flask app on port 5000
    