import click
from maihem.clients import Maihem
from maihem.utils.utils import import_wrapper_function, create_project_folder
from maihem.errors import RequestValidationError


# Create the main CLI group
@click.group()
@click.option(
    "--env",
    type=click.Choice(["local", "staging", "production"]),
    default="production",
    help="Environment to use (default: production)",
)
@click.pass_context
def cli(ctx, env):
    """Maihem CLI"""
    try:
        ctx.obj = Maihem(env=env)
    except RequestValidationError as e:
        click.echo(e)
        ctx.exit(1)


# Target agent commands
@cli.group()
def target_agent():
    """Manage target agents"""
    pass


@target_agent.command()
@click.option("--name", required=True, help="Unique name of the target agent")
@click.option("--label", help="Label for the target agent (optional)")
@click.option("--role", required=True, help="Role of the target agent")
@click.option("--description", required=True, help="Description of the target agent")
@click.option("--language", default="en", help="Language (default: en). Follow ISO 639")
@click.pass_obj
def create(maihem_client, name, label, role, description, language):
    """Create a target agent"""
    maihem_client.create_target_agent(
        name=name, label=label, role=role, description=description, language=language
    )
    create_project_folder(name)


# Test commands
@cli.group()
def test():
    """Manage tests"""
    pass


@test.command()
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
@click.pass_obj
def create(
    maihem_client,
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
    module_list = [m.strip() for m in modules.split(",")]
    maihem_client.create_test(
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
@click.pass_obj
def run(
    maihem_client,
    name,
    label,
    test_name,
    wrapper_function_path,
    concurrent_conversations,
):
    """Run a test"""
    wrapper_function = import_wrapper_function(wrapper_function_path)
    maihem_client.run_test(
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
@click.pass_obj
def get(maihem_client, test_name, test_run_name):
    """Get test run results"""
    test_run_results = maihem_client.get_test_run_result(
        test_name=test_name, test_run_name=test_run_name
    )
    click.echo(test_run_results)


if __name__ == "__main__":
    cli()
