Technical Documentation
Overview
This project is a web application built using Flask and the OpenAI API. It features functionalities such as login, chat, image generation, speech generation, and downloading conversations. Below are the details of the files and their respective functionalities.

Files and Functionality
1. app.py
Purpose: Main Flask application logic.
Author: Vijay Shrestha
Date: 2024/06/01
Key Components:
Environment Variables: Loaded from .env file (e.g., OPENAI_API_KEY, APP_PASSWORD).
Routes:
/login: Handles user login.
/logout: Logs out the user and clears session data.
/: Main page, redirects to login if not authenticated.
/chat: Processes user input and interacts with the OpenAI API.
/download: Allows downloading the conversation as a text file.
/generate-image: Generates images using the OpenAI API.
/generate-speech: Generates speech audio using the OpenAI API.
Memory Management: Manages conversation history and generated audio files.
2. index.html
Purpose: Main interface for the chat functionality.
Author: Vijay Shrestha
Date: 2024/06/01
Key Components:
Form Elements:
Text input for user messages.
File input for uploading files.
Buttons for sending messages, generating images, generating speech, downloading conversations, and logging out.
Dropdowns for selecting voice and language for speech generation.
JavaScript:
Handles form submission, API requests, and DOM manipulation for chat interactions.
Event listeners for buttons (send, generate image, generate speech, download, logout).
3. login.html
Purpose: Login page for access control.
Author: Vijay Shrestha
Date: 2024/06/01
Key Components:
Form Elements:
Password input for user authentication.
Button to submit the login form.
Error Handling: Displays error messages if the login fails.
4. styles.css
Purpose: CSS styles for the web application's layout and appearance.
Author: Vijay Shrestha
Date: 2024/06/01
Key Styles:
Body and Container: Styles for overall layout, centering, and responsiveness.
Form Elements: Input fields, buttons, file inputs with custom styles, and dropdowns.
Chat Container: Styles for displaying messages, including user and API messages, with appropriate colors and alignment.
Login Page: Specific styles for the login form and error messages.
5. .env
Purpose: Environment variables file (not provided for security reasons).
Details:
Contains sensitive information like OPENAI_API_KEY and APP_PASSWORD.
Setup and Usage
Prerequisites
Python 3.x
Flask
Requests library
Python-dotenv
Installation
Clone the repository.
Install the required Python libraries:
bash
Copy code
pip install flask requests python-dotenv
Create a .env file in the root directory with the following content:
env
Copy code
OPENAI_API_KEY=your_openai_api_key
APP_PASSWORD=your_app_password
Running the Application
Start the Flask application:
bash
Copy code
python app.py
Open your web browser and navigate to http://127.0.0.1:5000/.
Login with the password specified in the .env file.
Interact with the application by sending messages, generating images, generating speech, and downloading conversations.
Security Considerations
Ensure the secret_key in app.py is changed to a secure value.
Keep the .env file secure and do not expose it in public repositories.
Future Improvements
Implement more robust error handling.
Enhance the UI/UX for better user interaction.
Add more language support for speech generation.