# Website Question App

This project is a simple web application that allows users to input a question, select either the ChatGPT or Ollama model, and display the streaming response from the selected API. The application is built using Flask and provides a user-friendly interface for interacting with AI models.

## Project Structure

```
website-question-app
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── templates
│   │   └── index.html
│   ├── static
│   │   └── styles.css
│   └── utils
│       └── api_handler.py
├── requirements.txt
├── .env
└── README.md
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd website-question-app
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies**:
   ```
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   Create a `.env` file in the root directory and add your API keys and any other necessary configuration settings.

6. **Run the application**:
   ```
   python app/main.py
   ```

7. **Access the application**:
   Open your web browser and go to `http://localhost:5000` to interact with the application.

## Usage

- Enter your question in the input field.
- Select the desired model (ChatGPT or Ollama) from the dropdown menu.
- Click the "Submit" button to receive a streaming response from the selected API.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.