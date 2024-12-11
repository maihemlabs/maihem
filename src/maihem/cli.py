import argparse

from maihem.clients import Maihem
from maihem.utils.utils import import_wrapper_function, create_project_folder


def create_target_agent(target_agent_subparsers):
    """Create a target agent in CLI"""

    create_target_agent_parser = target_agent_subparsers.add_parser(
        "create", help="Create a target agent"
    )
    create_target_agent_parser.add_argument(
        "--name", type=str, required=True, help="Unique name of the target agent"
    )
    create_target_agent_parser.add_argument(
        "--label", type=str, help="Label for the target agent (optional)"
    )
    create_target_agent_parser.add_argument(
        "--role", type=str, required=True, help="Role of the target agent"
    )
    create_target_agent_parser.add_argument(
        "--description", type=str, required=True, help="Description of the target agent"
    )
    create_target_agent_parser.add_argument(
        "--language",
        type=str,
        default="en",
        help="Language (default: en). Follow ISO 639",
    )


def create_test(test_subparsers):
    """Create a test in CLI"""

    create_test_parser = test_subparsers.add_parser("create", help="Create a test")
    create_test_parser.add_argument(
        "--name", type=str, required=True, help="Name of the test"
    )
    create_test_parser.add_argument(
        "--label", type=str, help="Label for the test (optional)"
    )
    create_test_parser.add_argument(
        "--target_agent_name", type=str, required=True, help="Name of the target agent"
    )
    create_test_parser.add_argument(
        "--initiating_agent",
        type=str,
        choices=["maihem", "target"],
        default="maihem",
        help="Initiating agent (maihem or target)",
    )
    create_test_parser.add_argument(
        "--modules", type=str, required=True, help="Modules to use"
    )
    create_test_parser.add_argument(
        "--documents_path",
        type=str,
        required=True,
        help="Path to the folder with documents",
    )
    create_test_parser.add_argument(
        "--number_conversations",
        type=int,
        required=True,
        help="Number of conversations",
    )
    create_test_parser.add_argument(
        "--conversation_turns_max",
        type=int,
        default=10,
        help="Max turns per conversation (default: 10)",
    )


def run_test(test_subparsers):
    """Run a test in CLI"""

    run_test_parser = test_subparsers.add_parser("run", help="Run a test")
    run_test_parser.add_argument(
        "--name", type=str, required=True, help="Name of the test run"
    )
    run_test_parser.add_argument(
        "--label", type=str, help="Label for the test run (optional)"
    )
    run_test_parser.add_argument(
        "--test_name", type=str, required=True, help="Name of the test"
    )
    run_test_parser.add_argument(
        "--wrapper_function_path",
        type=str,
        default="wrapper_function.py",
        help="Path to the wrapper function",
    )


def test_run_get(test_run_subparsers):
    """Get test run results in CLI"""

    get_test_run_results_parser = test_run_subparsers.add_parser(
        "get", help="Get test run results"
    )
    get_test_run_results_parser.add_argument(
        "--test_name", type=str, required=True, help="Name of the test"
    )
    get_test_run_results_parser.add_argument(
        "--test_run_name", type=str, required=True, help="Name of the test run"
    )


def main():
    parser = argparse.ArgumentParser(prog="maihem", description="Maihem CLI")
    parser.add_argument(
        "--env",
        choices=["local", "staging", "production"],
        default="production",
        help="Environment to use (default: production)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add subparsers

    # Target agent
    target_agent_parser = subparsers.add_parser(
        "target_agent", help="Manage target agents"
    )
    target_agent_subparsers = target_agent_parser.add_subparsers(
        dest="action", help="Target agent actions"
    )
    create_target_agent(target_agent_subparsers)

    # Test
    test_parser = subparsers.add_parser("test", help="Manage tests")
    test_subparsers = test_parser.add_subparsers(dest="action", help="Test actions")
    create_test(test_subparsers)
    run_test(test_subparsers)

    # Test run
    test_run_parser = subparsers.add_parser("test_run", help="Manage tests runs")
    test_run_subparsers = test_run_parser.add_subparsers(
        dest="action", help="Test run actions"
    )
    test_run_get(test_run_subparsers)

    # Parse arguments
    args = parser.parse_args()

    # Create Maihem client
    maihem_client = Maihem(env=args.env)

    # Handle commands
    if args.command == "target_agent" and args.action == "create":
        maihem_client.create_target_agent(
            name=args.name,
            label=args.label,
            role=args.role,
            description=args.description,
            language=args.language,
        )

        create_project_folder(args.name)

    elif args.command == "test" and args.action == "create":
        module_list = args.modules.split(",").replace(" ", "")

        maihem_client.create_test(
            name=args.name,
            label=args.label,
            modules=module_list,
            target_agent_name=args.target_agent_name,
            initiating_agent=args.initiating_agent,
            # documents_path=args.documents_path,
            conversation_turns_max=args.conversation_turns_max,
            number_conversations=args.number_conversations,
        )
    elif args.command == "test" and args.action == "run":
        # Import wrapper function from the path
        wrapper_function = import_wrapper_function(args.wrapper_function_path)

        maihem_client.run_test(
            name=args.name,
            label=args.label,
            test_name=args.test_name,
            wrapper_function=wrapper_function,
        )
    elif args.command == "test_run" and args.action == "get":
        test_run_results = maihem_client.get_test_run_result(
            test_name=args.test_name, test_run_name=args.test_run_name
        )
        print(test_run_results)
    else:
        parser.print_help()
