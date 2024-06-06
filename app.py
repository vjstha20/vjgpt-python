from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from dotenv import load_dotenv
import os
import requests
from pathlib import Path
import time

# Author: Vijay Shrestha
# Date: 2024/06/01
# Functionality: This file contains the main Flask application logic including routes for login, chat, image generation, speech generation, and downloading conversations.

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
api_key = os.getenv('OPENAI_API_KEY')
app_password = os.getenv('APP_PASSWORD')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a secure key

headers = {
    "Authorization": f"Bearer {api_key}"
}

# Initialize conversation memory
memory = []
audio_files = []  # To keep track of generated audio files

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == app_password:
            session['logged_in'] = True
            memory.clear()  # Clear memory on new session
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid password')
    return render_template('login.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    memory.clear()  # Clear memory on logout
    
    # Delete all generated audio files
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            os.remove(audio_file)
    audio_files.clear()

    return redirect(url_for('login'))

# Route for the main page
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

# Route to handle OpenAI API requests
@app.route('/chat', methods=['POST'])
def chat():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_input = request.form.get('user_input')
    file = request.files.get('file')

    # Handle file upload
    if file:
        response = requests.post(
            'https://api.openai.com/v1/files',
            headers=headers,
            files={
                'file': (file.filename, file, 'multipart/form-data')
            },
            data={
                'purpose': 'fine-tune'
            }
        )
        if response.status_code == 200:
            file_id = response.json()['id']
            # Retrieve file content and add to memory
            response = requests.get(
                f'https://api.openai.com/v1/files/{file_id}/content',
                headers=headers
            )
            file_content = response.text
            memory.append({"role": "system", "content": f"File content: {file_content}"})

    # Add user input to memory
    memory.append({"role": "user", "content": user_input})

    # Send conversation history to OpenAI API and get response
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json={
            "model": "gpt-4",
            "messages": memory
        }
    )

    response_message = response.json()['choices'][0]['message']['content']
    memory.append({"role": "assistant", "content": response_message})

    return jsonify({'response': response_message})

# Route to download conversation
@app.route('/download', methods=['POST'])
def download():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conversation_text = '\n'.join(
        f"{msg['role']}: {msg['content']}" for msg in memory
    )
    
    return (
        conversation_text,
        {
            'Content-Disposition': 'attachment; filename="conversation.txt"',
            'Content-Type': 'text/plain'
        }
    )

# New route for generating images
@app.route('/generate-image', methods=['POST'])
def generate_image():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    data = request.get_json()
    prompt = data.get('prompt')

    response = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        json={
            'model': 'dall-e-3',  # or 'dall-e-3' if you have access
            'prompt': prompt,
            'n': 1,
            'size': '1024x1024'
        }
    )

    if response.status_code == 200:
        image_url = response.json()['data'][0]['url']
        return jsonify({'image_url': image_url})
    else:
        return jsonify({'error': 'Failed to generate image'}), response.status_code

# New route for generating speech
@app.route('/generate-speech', methods=['POST'])
def generate_speech():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    data = request.get_json()
    text = data.get('text')
    voice = data.get('voice', 'alloy')
    language = data.get('language', 'en')

    # Generate a unique file name using the current timestamp
    unique_filename = f"speech_{int(time.time())}.mp3"
    speech_file_path = Path(f'static/{unique_filename}')
    
    response = requests.post(
        'https://api.openai.com/v1/audio/speech',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        json={
            'model': 'tts-1-hd',
            'voice': voice,
            'input': text
        }
    )

    if response.status_code == 200:
        with open(speech_file_path, 'wb') as f:
            f.write(response.content)
        audio_files.append(speech_file_path)  # Keep track of the audio file
        return jsonify({'audio_url': url_for('static', filename=unique_filename)})
    else:
        return jsonify({'error': 'Failed to generate speech'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
