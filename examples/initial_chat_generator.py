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

print(data)