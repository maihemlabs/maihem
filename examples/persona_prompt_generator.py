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
persona = {
    'mood': "angry",
    'age': "30-40",
    'gender': "male",
    'ethnicity': "white",
    'disability': "none",
    'income': "high",
    'education': "college degree",
    'marital_status': "married",
    'children': "2",
    'employment': "employed",
    'housing': "rent",
    'occupation': "data scientist",
    'location': "New York",
    'customer_name': "John Doe",
  }

# Create data generator object
dg = mh.DataGenerator()

# Generate list of prompts for defined persona
data = dg.generate_prompts(intent, persona, model_temperature=0.8, n_calls=3, n_prompts_per_call=2)
print(data)