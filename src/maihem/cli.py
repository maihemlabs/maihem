import click
from maihem.clients import MaihemClient
from maihem.utils.utils import import_wrapper_function, create_project_folder
from maihem.api_client.maihem_client.models.environment import Environment


# Move login command before main group initialization
@click.group()
def cli():
    """Maihem CLI"""
    pass


@cli.command()
@click.argument("token")
def login(token: str):
    """Log in to Maihem using your API token."""
    try:
        client = MaihemClient(api_key=token)
        click.echo(f"✨ Successfully logged in")
        click.echo("🔒 Token stored securely in cache")
    except Exception as e:
        click.echo(f"❌ Login failed: {str(e)}")


@cli.command()
@click.argument("test_name")
@click.option("--env", default="production", help="Environment to use")
def generate_wrapper(env, test_name):
    """Generate a wrapper function for a test"""
    client = MaihemClient(env=env)
    client.generate_wrapper_function(test_name=test_name)
    click.echo(f"✨ Successfully generated wrapper function for test '{test_name}'")


@cli.group()
def target_agent():
    """Manage target agents"""
    pass


@target_agent.command()
@click.option("--env", default="production", help="Environment to use")
@click.option("--name", required=True, help="Unique name of the target agent")
@click.option("--label", help="Label for the target agent (optional)")
@click.option("--role", required=True, help="Role of the target agent")
@click.option("--description", required=True, help="Description of the target agent")
@click.option("--language", default="en", help="Language (default: en). Follow ISO 639")
def create(env, name, label, role, description, language):
    """Create a target agent"""
    client = MaihemClient(env=env)
    client.add_target_agent(
        name=name, label=label, role=role, description=description, language=language
    )
    create_project_folder(name)


# Test commands
@cli.group()
def test():
    """Manage tests"""
    pass


@test.command()
@click.option("--env", default="production", help="Environment to use")
@click.option("--name", required=True, help="Name of the test")
@click.option("--label", help="Label for the test (optional)")
@click.option("--target-agent-name", required=True, help="Name of the target agent")
@click.option(
    "--initiating-agent",
    type=click.Choice(["maihem", "target"]),
    default="maihem",
    help="Initiating agent (maihem or target)",
)
@click.option("--modules", required=True, help="Modules to use")
@click.option(
    "--documents-path", required=False, help="Path to the folder with documents"
)
@click.option(
    "--number-conversations", type=int, required=True, help="Number of conversations"
)
@click.option(
    "--conversation-turns-max",
    type=int,
    default=10,
    help="Max turns per conversation (default: 10)",
)
@click.option(
    "--maihem-behavior-prompt",
    help="Prompt for the maihem agent behavior",
)
@click.option(
    "--maihem-goal-prompt",
    help="Describes the goal of the simulated personas",
)
@click.option(
    "--maihem-population-prompt",
    help="Describes the desired population of simulated personas",
)
def create(
    env,
    name,
    label,
    target_agent_name,
    initiating_agent,
    modules,
    documents_path,
    number_conversations,
    conversation_turns_max,
    maihem_behavior_prompt,
    maihem_goal_prompt,
    maihem_population_prompt,
):
    """Create a test"""
    client = MaihemClient(env=env)
    module_list = [m.strip() for m in modules.split(",")]
    client.create_test(
        name=name,
        label=label,
        modules=module_list,
        target_agent_name=target_agent_name,
        initiating_agent=initiating_agent,
        documents_path=documents_path,
        conversation_turns_max=conversation_turns_max,
        number_conversations=number_conversations,
        maihem_behavior_prompt=maihem_behavior_prompt,
        maihem_goal_prompt=maihem_goal_prompt,
        maihem_population_prompt=maihem_population_prompt,
    )


@test.command()
@click.option("--env", default="production", help="Environment to use")
@click.option("--name", required=True, help="Name of the test run")
@click.option("--label", help="Label for the test run (optional)")
@click.option("--test-name", required=True, help="Name of the test")
@click.option(
    "--wrapper-function-path",
    default="wrapper_function.py",
    help="Path to the wrapper function",
)
@click.option(
    "--concurrent-conversations",
    type=int,
    default=10,
    help="Number of concurrent conversations",
)
def run(env, name, label, test_name, wrapper_function_path, concurrent_conversations):
    """Run a test"""
    client = MaihemClient(env=env)
    wrapper_function = import_wrapper_function(wrapper_function_path)
    client.run_test(
        name=name,
        label=label,
        test_name=test_name,
        wrapper_function=wrapper_function,
        concurrent_conversations=concurrent_conversations,
    )


# Test run commands
@cli.group()
def test_run():
    """Manage test runs"""
    pass


@test_run.command()
@click.option("--test-name", required=True, help="Name of the test")
@click.option("--test-run-name", required=True, help="Name of the test run")
def get(test_name, test_run_name):
    """Get test run results"""
    client = MaihemClient(env="production")
    test_run_results = client.get_test_run_result(
        test_name=test_name, test_run_name=test_run_name
    )
    click.echo(test_run_results)


if __name__ == "__main__":
    cli()
