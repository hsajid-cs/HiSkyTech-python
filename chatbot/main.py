from flask import Flask, request, jsonify, send_from_directory, render_template_string
import re
import random
import os

app = Flask(__name__)

class BasicBot:
    neg_responses = ("no", "dont", "stop", "don't")
    quit_responses = ("exit", "leave", "quit", "bye", "goodbye", "byebye")

    questions = ["How may I assist you?",
                 "What brings you here?",
                 "How can I help you?",
                 "What can I do for you today?",
                 "Is there something specific you need help with?"]
    
    def __init__(self) -> None:
        self.intro = {
            "asking_about_product": r'.*product.*',
            "asking_about_service": r'.*service.*',
            "asking_about_support": r'.*support.*',
            "asking_about_pricing": r'.*pricing.*',
            "asking_about_location": r'.*location.*',
            "asking_about_hours": r'.*hour.*'
        }
        self.name = None

    def greet(self, name):
        self.name = name.lower()
        return f"Hi, {self.name}, How can I help you?"

    def exit_chat(self, reply):
        if reply in self.quit_responses:
            return f"It was nice talking to you, {self.name}. Goodbye."
        return None

    def chat(self, response):
        response = response.lower()
        exit_message = self.exit_chat(response)
        if exit_message:
            return exit_message
        return self.find_match(response)

    def find_match(self, response):
        response = response.lower().strip()
        for key, value in self.intro.items():
            intent = key
            pattern = value
            match = re.match(pattern, response)
            if match and intent == "asking_about_product":
                return self.product_info()
            elif match and intent == "asking_about_service":
                return self.service_info()
            elif match and intent == "asking_about_support":
                return self.support_info()
            elif match and intent == "asking_about_pricing":
                return self.pricing_info()
            elif match and intent == "asking_about_location":
                return self.location_info()
            elif match and intent == "asking_about_hours":
                return self.hours_info()
        return self.no_match()

    def no_match(self):
        responses = [
            "Please tell me more.",
            "Tell me more!",
            "Why do you say that?",
            "I see. Can you elaborate?",
            "Interesting. Can you tell me more?",
            "I see. How do you think?",
            "Why?",
            "How do you think I feel when you say that?"
        ]
        return random.choice(responses)

    def product_info(self):
        responses = [
            "The product is a new product.",
            "The product is a top seller.",
            "The product is highly rated.",
            "The product has excellent reviews.",
            "The product comes with a one-year warranty."
        ]
        return random.choice(responses)
    
    def service_info(self):
        responses = [
            "We offer a variety of services.",
            "Our services are tailored to your needs.",
            "We provide top-notch service.",
            "Our services include consulting, implementation, and support.",
            "We have a range of premium services available."
        ]
        return random.choice(responses)
    
    def support_info(self):
        responses = [
            "Our support team is here to help you.",
            "We offer 24/7 support.",
            "You can reach our support team anytime.",
            "Our support team is known for quick and efficient responses.",
            "We provide support via phone, email, and live chat."
        ]
        return random.choice(responses)
    
    def pricing_info(self):
        responses = [
            "Our pricing is competitive and affordable.",
            "We offer various pricing plans to suit your needs.",
            "You can find our pricing details on our website.",
            "Contact us for a customized pricing plan.",
            "We offer discounts for bulk purchases."
        ]
        return random.choice(responses)

    def location_info(self):
        responses = [
            "We are located at 123 Main Street, Anytown.",
            "Our main office is in the city center.",
            "We have several locations across the country.",
            "You can find our location details on our website.",
            "Visit our office for a personal consultation."
        ]
        return random.choice(responses)

    def hours_info(self):
        responses = [
            "We are open from 9 AM to 5 PM, Monday to Friday.",
            "Our business hours are from 8 AM to 6 PM on weekdays.",
            "We are closed on weekends and public holidays.",
            "You can visit us during our business hours: 10 AM to 4 PM.",
            "Our support team is available 24/7."
        ]
        return random.choice(responses)

myBot = BasicBot()

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='chatbot.css') }}">
    <title>Simple Chatbot</title>
</head>
<body>
    <div id="chat-box">
    </div>
    <div class="input-box">
        <input type="text" id="user-input" placeholder="Type your message...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        function sendMessage() {
            const userInput = document.getElementById("user-input").value;
            const chatBox = document.getElementById("chat-box");

            if (userInput.trim() === "") {
                return;
            }

            // Display user message
            const userMessage = document.createElement("div");
            userMessage.className = "container darker";
            userMessage.innerHTML = `<img src="{{ url_for('static', filename='user_avatar.jpg') }}" alt="Avatar" class="right"><p>${userInput}</p><span class="time-right">${new Date().toLocaleTimeString()}</span>`;
            chatBox.appendChild(userMessage);

            // Scroll chat box to bottom
            chatBox.scrollTop = chatBox.scrollHeight;

            // Send message to server
            fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: userInput })
            })
            .then(response => response.json())
            .then(data => {
                // Display bot response
                const botMessage = document.createElement("div");
                botMessage.className = "container";
                botMessage.innerHTML = `<img src="{{ url_for('static', filename='bot_avatar.jpg') }}" alt="Avatar"><p>${data.response}</p><span class="time-left">${new Date().toLocaleTimeString()}</span>`;
                chatBox.appendChild(botMessage);

                // Scroll chat box to bottom
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch(error => console.error("Error:", error));

            // Clear user input
            document.getElementById("user-input").value = "";
        }

        // Initialize chat with asking for the user's name
        window.onload = function() {
            const chatBox = document.getElementById("chat-box");
            const botMessage = document.createElement("div");
            botMessage.className = "container";
            botMessage.innerHTML = `<img src="{{ url_for('static', filename='bot_avatar.jpg') }}" alt="Avatar"><p>What's your name?</p><span class="time-left">${new Date().toLocaleTimeString()}</span>`;
            chatBox.appendChild(botMessage);
        }
    </script>
</body>
</html>
    ''')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({"response": "Message is required"}), 400
    
    if myBot.name is None:
        myBot.name = message
        response = myBot.greet(myBot.name)
    else:
        response = myBot.chat(message)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
