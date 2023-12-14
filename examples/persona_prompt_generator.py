import os
import maihem as mh


# Set API key manually
os.environ['MAIHEM_API_KEY'] = '<your_maihem_api_key>'

# Parameter dictionary for persona
persona = {
    'intent': "credit card got blocked",
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
    'occupation': "banker",
    'location': "New York",
    'sector_name': "retail banking",
    'customer_name': "John Doe",
  }

# Create data generator object
dg = mh.DataGenerator()

# Generate list of prompts for defined persona
data = dg.generate_prompts(persona, model_temperature=0.8, n_calls=3, n_prompts_per_call=2)
print(data)