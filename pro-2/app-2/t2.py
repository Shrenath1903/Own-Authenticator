from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# URL of the first app (Password Generator)
PASSWORD_GENERATOR_URL = 'http://localhost:5000/get_password'

@app.route('/', methods=['GET', 'POST'])
def validate_password():
    if request.method == 'POST':
        # Get user input from the form
        user_input = request.form.get('password')
        
        if not user_input:
            return render_template('index.html', message="Password is required!", status="error")

        # Get the current password from the first app
        try:
            response = requests.get(PASSWORD_GENERATOR_URL)
            response.raise_for_status()
            current_password = response.json().get('password')
        except requests.RequestException as e:
            return render_template('index.html', message="Failed to connect to Password Generator!", status="error")

        # Compare passwords
        print("user_input:",user_input)
        print("current_password:",current_password)
        if user_input == current_password:
            return render_template('index.html', message="Unlocked!", status="success")
        else:
            return render_template('index.html', message="Check the password!", status="error")

    # Render the form for GET requests
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
