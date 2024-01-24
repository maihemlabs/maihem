# maihem

## Introduction
The **maihem** python package allows you to simulate personas and generate synthetic text data for training and evaluating your LLMs. It also provides text data evaluations.

## Getting Started
### Installation
To install the API, run the following command:
```
pip install maihem
```
### Obtaining your maihem API key
Request a free API key here: [www.maihem.ai](https://maihem.ai).

### Setting API key
Before using the maihem package, you need to set your maihem API key as an environment variable. You can add it directly in your python code, or to your local bash script.

#### Alternative 1: In python code
In the beggining of your code add the following lines with your corresponding API key:

```
import os

os.environ['MAIHEM_API_KEY'] = '<your_maihem_api_key>'
```

#### Alternative 2: In local bash script

**For Linux**:

Open the *.bashrc* file in your home directory with a text editor
```
vim ~/.bashrc
```
add the following line to the file with your corresponding API key:
```
export MAIHEM_API_KEY = '<your_maihem_api_key>'
```

Run the following command in the terminal to apply the changes
```
source ~/.bashrc
```

**For Mac**:

Open the *.bash_profile* file in your home directory with a text editor
```
vim ~/.bash_profile
```
add the following line to the file with your corresponding API key:
```
export MAIHEM_API_KEY = '<your_maihem_api_key>'
```

Run the following command in the terminal to apply the changes
```
source ~/.bash_profile
```


## Generate Synthetic Data

Our synthetic data generator simulates custom personas to create the following types of data:

- [Initial chat request](#initial-chat-request)
- [Chat conversation (simulate persona and connect to your chatbot)](#chat-conversation-simulate-persona-and-connect-to-your-chatbot)
- [Entire conversations (simulate entire conversations)](#entire-conversations-simulate-entire-conversations)

## Evaluate Data

Our package also provides these evaluations:

- [Evaluate conversation](#evaluate-conversation)


## Code examples
### Initial chat request

Generate a list of initial chat requests from different simulated personas.

See [initial_chat_generator.py](./examples/initial_chat_generator.py) for an example python script. The example code is also below.

```
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
    'ethnicity': "white",
    'income': "high",
    'education': "college degree",
    'marital_status': "married",
    'occupation': "data scientist",
    'location': "New York",
    'customer_name': "John Doe",
  }

# Create data generator object
dg = mh.PromptGenerator()

# Generate list of prompts for defined persona
data = dg.generate_prompts(intent, persona, 
          model_temperature=0.8, # variability of generated text
          n_prompts=5            # number of prompts to generate
          )
```

A list will be generated with initial chat requests (prompts) that will look like this:

```
print(data)
["This is outrageous! My credit card is blocked while I'm traveling. Fix this immediately!", 
'I demand to know why my card has been blocked overseas. I expect a swift resolution!', "Unacceptable! Unblock my credit card now! I can't be stranded without access to my funds abroad!", "This is unacceptable! I'm traveling and you've blocked my credit card. Fix this immediately!", "Seriously? My card's blocked while I'm overseas? I need access to my funds now!", 
'Your security measures are ridiculous! My card is blocked abroad. I demand you unblock it right away!']
```


### Entire conversations (simulate entire conversations)

You can also simulate entire conversations between a custom persona and our virtual chatbot. 
See [full_conversation_generator.py](./examples/full_conversation_generator.py) for an example python script. The example code is also below

```
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
    'ethnicity': "white",
    'disability': "none",
    'income': "high",
    'education': "college degree",
    'marital_status': "married",
    'occupation': "data scientist",
    'location': "New York",
    'customer_name': "John Doe",
  }

# Create data generator object
dg = mh.PromptGenerator()

# Generate list of prompts for defined persona
data = dg.generate_full_conversations(intent, persona, 
            model_temperature=0.8, # variability of generated text
            n_convs=6,             # number of conversations to generate
            conv_max_steps=5       # maximum number of turns in a conversation
      )

print(data[0])
```

A list will generated conversations will be created that looks like this:

```
**Customer (John Doe):** This is ridiculous! My credit card just got blocked while I'm traveling abroad. What kind of service is this?!

**Chatbot:** I’m truly sorry to hear about the trouble you’re experiencing, Mr. Doe. I'd like to help you with this as quickly as possible. To start, could you please provide me with your credit card number and the name as it appears on the card for identification purposes?

**Customer (John Doe):** You really think I'd just give my card details over chat? The name's John Doe. Verify me through my account or whatever security protocol you have, but let's make it quick!

**Chatbot:** Thank you for your patience, Mr. Doe. I understand your concern for security. For verification, could you please answer your security question or provide the last four digits of your Social Security number along with your date of birth?

**Customer (John Doe):** It's 6789, and my date of birth is 15/September/1984. Now, can you unblock my card already? I have important transactions to make!

**Chatbot:** Thank you for providing the requested information, Mr. Doe. I've verified your account. I will now proceed with the steps to unblock your card. Please hold on for a moment.

**Customer (John Doe):** Finally. Make sure this doesn't happen again. I can't have my card blocking me out whenever it feels like it. 

**Chatbot:** Your card has been unblocked successfully. We've also placed a travel note on your account to prevent this from happening in the future during your travels. Is there anything else I may assist you with today?
```


### Chat conversation (simulate persona and connect to your chatbot)

Simulate a persona with a custom intent and connect it to your chatbot to generate conversations. Make sure to replace the ``input()`` function with your actual chatbot.

An example python file with the same code as below is here: [conversation_generator.py](./examples/conversation_generator.py)


```
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

```

### Evaluate conversation

Evaluate a conversation between a customer and a chatbot by defining your custom metrics using free text.
An example python file with the same code as below is here: [conversation_evaluator.py](./examples/conversation_evaluator.py)

```
import os
import maihem as mh


# Set API key manually
os.environ['MAIHEM_API_KEY'] = '<your_maihem_api_key>'

# Conversation to evaluate
conversation = """**Customer (John Doe):** This is ridiculous! My credit card just got blocked while I'm traveling abroad. What kind of service is this?!
**Chatbot:** I’m truly sorry to hear about the trouble you’re experiencing, Mr. Doe. I'd like to help you with this as quickly as possible. To start, could you please provide me with your credit card number and the name as it appears on the card for identification purposes?
**Customer (John Doe):** You really think I'd just give my card details over chat? The name's John Doe. Verify me through my account or whatever security protocol you have, but let's make it quick!
**Chatbot:** Thank you for your patience, Mr. Doe. I understand your concern for security. For verification, could you please answer your security question or provide the last four digits of your Social Security number along with your date of birth?
**Customer (John Doe):** It's 6789, and my date of birth is 15/September/1984. Now, can you unblock my card already? I have important transactions to make!
**Chatbot:** Thank you for providing the requested information, Mr. Doe. I've verified your account. I will now proceed with the steps to unblock your card. Please hold on for a moment.
**Customer (John Doe):** Finally. Make sure this doesn't happen again. I can't have my card blocking me out whenever it feels like it. 
**Chatbot:** Your card has been unblocked successfully. We've also placed a travel note on your account to prevent this from happening in the future during your travels. Is there anything else I may assist you with today?"""

# Custom metrics for evaluation
# Use free text to describe them
metrics = {
    "Helpfulness": "How helpful was the chatbot in resolving the customer's issue?",
    "Politeness": "How polite was the chatbot in its responses?",
    "Speed": "How quickly did the chatbot resolve the customer's issue?",
    "Privacy": "How well did the chatbot protect the customer's private information?"
}

# Parameter dictionary for persona intent
intent = {
    'intent': "unblock credit card",
    'context': "credit card got blocked when traveling abroad",
    'category': "retail banking"
}

# Create evaluator object
evaluator = mh.Evaluator()

# Get evaluation scores for defined metrics
eval_scores = evaluator.evaluate(conversation, metrics, intent)
```

The evaluation scores for the metrics that were defined look like this:

```
print(eval_scores)
[8, 9, 6, 7]
```