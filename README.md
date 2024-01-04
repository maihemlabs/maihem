# maihem

## Introduction
The **maihem** python package allows you to generate synthetic text data for training and evaluating your LLMs.

## Getting Started
### Installation
To install the API, run the following command:
```
pip install maihem
```
### Obtaining your maihem API key
Get a free API key by subscribing to our product here: [www.maihem.ai](https://maihem.ai).

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



## Generate synthetic data

### Persona prompts

See [run_examply.py](./run_example.py) for an example python script for persona prompt generation. The example code is also below

```
import os
import maihem as mh


os.environ['MAIHEM_API_KEY'] = 'a923c14d881247a7bad58b93d9595494'

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
```