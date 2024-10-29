import click
import importlib.util
import sys
from pathlib import Path
from maihem.simulator import Simulator


@click.group()
def cli():
    """MAIHEM CLI tool for LLM testing"""
    pass


def load_chat_function():
    """Load the chat_function from run_maihem.py in the current directory"""
    run_maihem_path = Path("./run_maihem.py")
    if not run_maihem_path.exists():
        click.echo("Error: run_maihem.py not found in current directory", err=True)
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("run_maihem", run_maihem_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "chat_function"):
        click.echo("Error: chat_function not found in run_maihem.py", err=True)
        sys.exit(1)

    return module.chat_function


@cli.command()
@click.option(
    "--target-agent-identifier",
    "-t",
    required=True,
    help="Identifier for the target agent",
)
@click.option(
    "--maihem-agent-identifier",
    "-m",
    required=True,
    help="Identifier for the maihem agent",
)
@click.option(
    "--config-path", "-c", default="./config.yaml", help="Path to config file"
)
def dev(target_agent_identifier, maihem_agent_identifier, config_path):
    """Run MAIHEM in development mode"""
    chat_function = load_chat_function()
    conversation = Simulator.conversation(
        chat_function,
        target_agent_identifier=target_agent_identifier,
        maihem_agent_identifier=maihem_agent_identifier,
        config_path=config_path,
    )
    click.echo(conversation.messages)
    click.echo(conversation.evaluation)


@cli.command()
@click.option(
    "--target-agent-identifier",
    "-t",
    required=True,
    help="Identifier for the target agent",
)
@click.option("--test-identifier", "-test", required=True, help="Test identifier")
@click.option(
    "--config-path", "-c", default="./config.yaml", help="Path to config file"
)
def test(target_agent_identifier, test_identifier, config_path):
    """Run MAIHEM in test mode"""
    chat_function = load_chat_function()
    conversations = Simulator.test(
        chat_function,
        target_agent_identifier=target_agent_identifier,
        test_identifier=test_identifier,
        config_path=config_path,
    )
    click.echo(conversations[0].messages)
    click.echo(conversations[0].evaluation)


if __name__ == "__main__":
    cli()
