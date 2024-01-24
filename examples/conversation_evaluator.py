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

print(eval)