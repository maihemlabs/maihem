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
        config = cls._load_config(
            config_path=config_path, 
            target_agent_identifier=target_agent_identifier, 
            identifier=maihem_agent_identifier,
            dev_mode=True
        )
        
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
        
        if (
            "documents" in config["maihem_agent"][maihem_agent_identifier] and
            len(config["maihem_agent"][maihem_agent_identifier]["documents"]) > 0 and
            "rag" in config["maihem_agent"][maihem_agent_identifier]["metric"] 
        ):
            target_agent.add_documents(documents=config["maihem_agent"][maihem_agent_identifier]["documents"])
        
        metrics_config = {config["maihem_agent"][maihem_agent_identifier]["metric"]: 1}
        
        test = maihem_client.upsert_test(
            identifier=maihem_agent_identifier,
            initiating_agent=config["maihem_agent"][maihem_agent_identifier]["initiating_agent"],
            name=config["maihem_agent"][maihem_agent_identifier]["name"],
            maihem_agent_behavior_prompt=config["maihem_agent"][maihem_agent_identifier]["behavior_prompt"],
            conversation_turns_max=config["maihem_agent"][maihem_agent_identifier]["conversation_turns_max"],
            metrics_config=metrics_config,
            target_agent_identifier=target_agent_identifier
        )
        
        test_run = maihem_client.create_test_run_dev_mode(
            test_identifier=test.identifier,
            target_agent=target_agent
        )
        
        conversations = maihem_client.get_test_run_result_conversations(test_run.id)
        
        return SimulatedConversation(conversations, 0)
    
    @classmethod
    def test(
        cls, 
        chat_function: Callable,
        target_agent_identifier: str,
        test_identifier: str,      
        config_path: str = "./config.yaml",    
    ) -> SimulatedConversation:
        """Simulate a single conversation between the Maihem Agent and the Target Agent"""
        logger = get_logger()
        
        # Read config.yaml file
        config = cls._load_config(
            config_path=config_path, 
            target_agent_identifier=target_agent_identifier,
            identifier=test_identifier, 
            dev_mode=False
        )
        
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

        metrics_config = {metric: 10 for metric in config["test"][test_identifier]["metrics"]}

        test = maihem_client.upsert_test(
            identifier=test_identifier,
            initiating_agent=config["test"][test_identifier]["initiating_agent"],
            name=config["test"][test_identifier]["name"],
            maihem_agent_behavior_prompt=config["test"][test_identifier]["behavior_prompt"],
            conversation_turns_max=config["test"][test_identifier]["conversation_turns_max"],
            metrics_config=metrics_config,
            target_agent_identifier=target_agent_identifier
        )

        test_run = maihem_client.create_test_run(
            test_identifier=test.identifier, 
            target_agent=target_agent,
            concurrent_conversations=len(config["test"][test_identifier]["metrics"])
        )

        conversations = maihem_client.get_test_run_result_conversations(test_run.id)
        conversations_transformed = [SimulatedConversation(conversations, i) for i in range(len(conversations.conversations))]

        return conversations_transformed

    @classmethod
    def _load_config(
        cls, 
        config_path: str, 
        target_agent_identifier: str,
        identifier: str,
        dev_mode: bool = True
    ) -> Dict:
        logger = get_logger()
        try:
            with open(config_path, "r") as file:
                config = yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error reading config file: {str(e)}")
            raise_config_file_error(f"Error reading config file: {str(e)}")

        try:
            # Check if required keys for target agent are present in config file
            assert "target_agent" in config, "'target_agent' key not found in config file"
            assert target_agent_identifier in config["target_agent"].keys(), f"Target agent '{target_agent_identifier}' not found in config file"
            
            for tg_ag_identifier, target_agent in config["target_agent"].items():
                assert "role" in target_agent, f"'role' key not found in target agent {tg_ag_identifier}"
                assert "industry" in target_agent, f"'industry' key not found in target agent {tg_ag_identifier}"
                assert "description" in target_agent, f"'description' key not found in target agent {tg_ag_identifier}"
                target_agent["name"] = target_agent.get("name")
                target_agent["language"] = target_agent.get("language")
                
                for key in target_agent.keys():
                    if key not in ["name", "role", "industry", "description", "language"]:
                        raise_config_file_error(f"Invalid key '{key}' found in target agent {identifier}")
                       
            if dev_mode:
                assert "maihem_agent" in config, "'maihem_agent' key not found in config file" 
                assert "metric" in config["maihem_agent"][identifier].keys(), f"'metric' key not found in {identifier}"
                assert identifier in config["maihem_agent"].keys(), f"Maihem agent '{identifier}' not found in config file"
            else:
                assert "test" in config, "'test' key not found in config file" 
                assert "metrics" in config["test"][identifier].keys(), f"'metrics' key not found in {identifier}"
                assert identifier in config["test"].keys(), f"Test '{identifier}' not found in config file"
            
            instance_type = "maihem_agent" if dev_mode else "test"
            for identifier, instance in config[instance_type].items():
                instance["name"] = instance.get("name")
                if dev_mode:
                    instance["metric"] = instance.get("metric")
                else:
                    assert isinstance(instance["metrics"], list), f"'metrics' key must be a list in {identifier}"
                    instance["metrics"] = instance.get("metrics")
                    assert len(instance["metrics"]) > 0, f"'metrics' key must have at least one metric in {identifier}"
                instance["behavior_prompt"] = instance.get("behavior_prompt")
                instance["initiating_agent"] = instance.get("initiating_agent")
                instance["conversation_turns_max"] = instance.get("conversation_turns_max")
                if "documents" in instance.keys():
                    instance["documents"] = instance.get("documents")
                    assert isinstance(instance["documents"], list), f"'documents' key must be a list in {identifier}"
                
                for key in instance.keys():
                    if key not in ["name", "metric", "metrics", "behavior_prompt", "initiating_agent", "conversation_turns_max", "documents"]:
                        raise_config_file_error(f"Invalid key '{key}' found in {identifier}")

        except Exception as e:
            logger.error(f"Error reading config file: {str(e)}")
            raise_config_file_error(f"Error reading config file: {str(e)}")
        
        return config 
