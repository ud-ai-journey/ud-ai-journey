from flask import Flask, render_template, jsonify, request
from voice_assistant import VoiceAssistant
import os

app = Flask(__name__)
assistant = VoiceAssistant()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    command = request.json.get('command')
    if command:
        # Process the command using the voice assistant
        response = assistant.process_command(command)
        if response is False:  # Exit command
            return jsonify({'response': 'Goodbye! Have a great day!'})
        return jsonify({'response': 'Command processed successfully'})
    return jsonify({'error': 'No command received'}), 400

@app.route('/get_time', methods=['GET'])
def get_time():
    time_info = assistant.get_current_time()
    return jsonify({'response': time_info})

@app.route('/search_wiki', methods=['POST'])
def search_wiki():
    query = request.json.get('query')
    if query:
        result = assistant.search_wikipedia(query)
        return jsonify({'response': result})
    return jsonify({'error': 'No query received'}), 400

@app.route('/tell_joke', methods=['GET'])
def tell_joke():
    joke = assistant.tell_joke()
    return jsonify({'response': joke})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
