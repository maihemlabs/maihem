from typing import List, Callable, Dict
import yaml

from maihem.errors import raise_config_file_error
from maihem.logger import get_logger


class Simulator:
    """
    Class to simulate conversations between the Maihem Agent and the Target Agent
    """
    
    @classmethod
    def conversation(
        cls, 
        chat_function: Callable,
        target_agent_identifier: str,
        maihem_agent_identifier: str,      
        config_path: str = "./config.yaml",    
    ):
        """Simulate a single conversation between the Maihem Agent and the Target Agent"""
        logger = get_logger()
        
        # Read config.yaml file
        config = cls._load_config(config_path, target_agent_identifier, maihem_agent_identifier)
        
        return config
    
    @classmethod
    def _load_config(
        cls, 
        config_path: str, 
        target_agent_identifier: str, 
        maihem_agent_identifier: str
    ) -> Dict:
        logger = get_logger()
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error reading config file: {str(e)}")    
            raise_config_file_error(f"Error reading config file: {str(e)}")
            
        try:
            assert "metric" in config, "'metric' key not found in config file"
            assert "target_agent" in config, "'target_agent' key not found in config file"
            assert "maihem_agent" in config, "'maihem_agent' key not found in config file"
            
            for identifier, target_agent in config["target_agent"].items():
                assert "role" in target_agent, f"'role' key not found in target agent {identifier}"
                assert "industry" in target_agent, f"'industry' key not found in target agent {identifier}"
                assert "description" in target_agent, f"'description' key not found in target agent {identifier}"
                
            assert target_agent_identifier in config["target_agent"].keys(), f"Target agent '{target_agent_identifier}' not found in config file"
            assert maihem_agent_identifier in config["maihem_agent"].keys(), f"Maihem agent '{maihem_agent_identifier}' not found in config file"
                       
        except Exception as e:
            logger.error(f"Error reading config file: {str(e)}")    
            raise_config_file_error(f"Error reading config file: {str(e)}")
            
        return config