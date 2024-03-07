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

## Examples of how to use MAIHEM

- [Simulate conversations between your chatbot and AI personas and evaluate conversations](examples/simulate_and_evaluate_convs.ipynb)
- [Log historical conversations and evaluate them](examples/log_and_evalaute_convs.ipynb)