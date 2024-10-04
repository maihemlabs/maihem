from typing import List, Callable, Dict
import yaml

from maihem.clients import Maihem
from maihem.errors import raise_config_file_error
from maihem.logger import get_logger
from maihem.schemas.tests import SimulatedConversation


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
    ) -> SimulatedConversation:
        """Simulate a single conversation between the Maihem Agent and the Target Agent"""
        logger = get_logger()
        
        # Read config.yaml file
        config = cls._load_config(config_path, target_agent_identifier, maihem_agent_identifier)
        
        maihem_client = Maihem()
        
        logger.info("Initiating conversation...")
        target_agent = maihem_client.upsert_target_agent(
            identifier=target_agent_identifier, 
            role=config["target_agent"][target_agent_identifier]["role"],
            industry=config["target_agent"][target_agent_identifier]["industry"],
            description=config["target_agent"][target_agent_identifier]["description"],
            name=config["target_agent"][target_agent_identifier]["name"],
            language=config["target_agent"][target_agent_identifier]["language"],
        )
        target_agent.set_chat_function(chat_function)
        
        metrics_config = {config["metric"]: 1}
        
        test = maihem_client.upsert_test(
            identifier=maihem_agent_identifier,
            initiating_agent=config["initiating_agent"],
            name=config["maihem_agent"][maihem_agent_identifier]["name"],
            maihem_agent_behavior_prompt=config["maihem_agent"][maihem_agent_identifier]["behavior_prompt"],
            conversation_turns_max=config["maihem_agent"][maihem_agent_identifier]["conversation_turns_max"],
            metrics_config=metrics_config
        )
        
        test_run = maihem_client.create_test_run_dev_mode(
            test_identifier=test.identifier,
            target_agent=target_agent
        )
        
        conversation = maihem_client.get_test_run_result_conversations(test_run.id)
        
        return SimulatedConversation(conversation)
    
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
            assert "initiating_agent" in config, "'initiating_agent' key not found in maihem_agent"
            assert "target_agent" in config, "'target_agent' key not found in config file"
            assert "maihem_agent" in config, "'maihem_agent' key not found in config file" 
            assert target_agent_identifier in config["target_agent"].keys(), f"Target agent '{target_agent_identifier}' not found in config file"
            assert maihem_agent_identifier in config["maihem_agent"].keys(), f"Maihem agent '{maihem_agent_identifier}' not found in config file"
            
            for identifier, target_agent in config["target_agent"].items():
                assert "role" in target_agent, f"'role' key not found in target agent {identifier}"
                assert "industry" in target_agent, f"'industry' key not found in target agent {identifier}"
                assert "description" in target_agent, f"'description' key not found in target agent {identifier}"
                target_agent["name"] = target_agent.get("name")
                target_agent["language"] = target_agent.get("language")
                
            for identifier, maihem_agent in config["maihem_agent"].items():
                maihem_agent["name"] = maihem_agent.get("name")
                maihem_agent["behavior_prompt"] = maihem_agent.get("behavior_prompt")
                maihem_agent["conversation_turns_max"] = maihem_agent.get("conversation_turns_max")
                       
        except Exception as e:
            logger.error(f"Error reading config file: {str(e)}")    
            raise_config_file_error(f"Error reading config file: {str(e)}")
            
        return config