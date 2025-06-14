from flask import Flask, render_template, jsonify, request
import datetime
import wikipedia
import random
import os

app = Flask(__name__)

def get_current_time():
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %B %d, %Y")
    return f"The current time is {time_str} on {date_str}"

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a fake noodle? An impasta!",
        "Why did the math book look so sad? Because it had too many problems!"
    ]
    return random.choice(jokes)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    command = request.json.get('command', '').lower()
    if not command:
        return jsonify({'error': 'No command received'}), 400

    try:
        # Process different types of commands
        if any(word in command for word in ['hello', 'hi', 'hey']):
            response = "Hello! How can I help you today?"
        elif any(word in command for word in ['time', 'date', 'today']):
            response = get_current_time()
        elif any(word in command for word in ['search', 'tell me about', 'what is']):
            # Extract search query
            query = command.replace("search for", "").replace("tell me about", "").replace("what is", "").strip()
            try:
                summary = wikipedia.summary(query, sentences=2)
                response = f"Here's what I found about {query}: {summary}"
            except:
                response = f"Sorry, I couldn't find information about {query}"
        elif any(word in command for word in ['joke', 'funny']):
            response = tell_joke()
        elif any(word in command for word in ['bye', 'goodbye', 'exit']):
            response = "Goodbye! Have a great day!"
        else:
            response = "I'm not sure how to help with that. Try asking for the time, searching Wikipedia, or asking for a joke!"

        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_time', methods=['GET'])
def get_time_route():
    return jsonify({'response': get_current_time()})

@app.route('/tell_joke', methods=['GET'])
def tell_joke_route():
    return jsonify({'response': tell_joke()})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
