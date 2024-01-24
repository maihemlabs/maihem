import os
import maihem as mh


# Set API key manually
os.environ['MAIHEM_API_KEY'] = '<your_maihem_api_key>'

# Parameter dictionary for intent
intent = {
    'intent': "unblock credit card",
    'context': "credit card got blocked when traveling abroad",
    'category': "retail banking"
}

# Parameter dictionary for persona
# Input any parameters as free text in dictionary
persona = {
    'mood': "angry",
    'age': "30-40",
    'gender': "male",
    'occupation': "data scientist",
    'location': "New York",
    'customer_name': "John Doe",
  }

# Create chat conversation persona agent
persona_agent = mh.ConversationGenerator()

# Initialize chat conversation persona agent with custom parameters
persona_agent.initialize(intent, persona, 
        model_temperature=0.8, # variability of generated text
        conv_max_steps=10,     # maximum number of turns in a conversation
        max_n_words=60)        # maximum number of words in a response

# Create loop for simulated persona agent to chat with your chatbot
for _ in range(10):
    # Input chatbot message in terminal for demo purposes
    message_chatbot = input("Type chatbot message: ")  # replace input with your chatbot
    print(f"Chatbot: {message_chatbot}")
    message_persona = persona_agent.chat(message_chatbot)
    if message_persona == "END":
        break
    print(f"Persona agent: {message_persona}")
