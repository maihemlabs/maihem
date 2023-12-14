import requests
import os
import warnings


class DataGenerator():
    """
    Class to generate synthetic data using the MAIHEM API
    """

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self._get_api_key()
        self.URL_API = "https://maihem-api-access.azure-api.net/checks"

    def _get_api_key(self):
        if os.getenv('MAIHEM_API_KEY') is not None:
            self.api_key = os.getenv('MAIHEM_API_KEY')
            self.headers['Ocp-Apim-Subscription-Key'] = self.api_key

        else:
            warnings.warn("MAIHEM_API_KEY not found in environment variables, please set manually with the set_api_key() function", 
                          APIKeyWarning)

    def set_api_key(self, key: str):
        """
        Set API key manually or read from OS environment variable
        """
        self.api_key = key
        self.headers['Ocp-Apim-Subscription-Key'] = self.api_key

    def generate_prompts(self, persona_params: dict, model_temperature: float, 
                         n_calls: int, n_prompts_per_call: int) -> list:
        """
        Generate data using persona parameters and model generator parameters
        """
        generator_params = {
            'sync_generation': False,
            'use_azure': False,
            'model_temperature': model_temperature,
            'n_calls': n_calls,
            'n_prompts_per_call': str(n_prompts_per_call)
        }

        self._check_params(persona_params, generator_params)

        item ={
            "persona": persona_params,
            "generator": generator_params
        }

        try:
            response = requests.post(self.URL_API + '/generator', headers=self.headers, json=item)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        try:
            data = response.json()['data']
            if generator_params['use_azure']:
                data_converted = list(data.values())
            else:
                data_converted = self._convert_response(data)
            
            return data_converted
        except:
            print(response)
            warnings.warn("No data was returned, check input parameters", NoResponseData)

    def _check_params(self, persona_params: dict, generator_params: dict):
        """
        Check if parameters are valid
        """
        assert type(persona_params) == dict, "persona_params must be a dictionary"
        assert type(generator_params) == dict, "generator_params must be a dictionary"

        for param in persona_params.keys():
            assert type(persona_params[param]) == str, "persona parameter must be a string"

        assert 'n_calls' in generator_params.keys(), "n_calls must be provided"
        assert 'n_prompts_per_call' in generator_params.keys(), "n_prompts_per_call must be provided"
        assert type(generator_params['model_temperature']) == float, "model_temperature must be a number"
        assert 0 <= generator_params['model_temperature'] <= 2 , "model_temperature must be between 0 and 2"

    def _convert_response(self, data: dict) -> list:
        """
        Convert response from API to a dictionary
        """
        data_conv = []
        for key,value in data.items():
            # Split responses
            s = value.split('\"')
            for i in range(1, (len(s)), 2):
                data_conv.append(s[i])

        return data_conv


class APIKeyWarning(UserWarning):
    pass


class NoResponseData(UserWarning):
    pass
