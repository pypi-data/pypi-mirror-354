import argparse
import asyncio
import json
import traceback
import os
import subprocess
from pathlib import Path
from loguru import logger as log
from aiohttp.client_exceptions import ClientPayloadError
from hackbot.utils import get_version, Endpoint
from hackbot.config import set_local_mode, set_dev_mode
from hackbot.hack import (
    authenticate,
    cli_run,
    cli_scope,
    cli_learn,
    cli_price,
    cli_report,
    HackbotAuthError,
)
from typing import Union, cast, Dict

__version__ = get_version()

GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
GREY = "\033[1;90m"
END = "\033[0m"


def add_common_arguments(parser: argparse.ArgumentParser, hide_dev_tool_help: bool = True):
    """Add common arguments to a parser."""
    parser.add_argument(
        "--auth-only", action="store_true", help="Only verify API key authentication"
    )
    parser.add_argument(
        "-s",
        "--source",
        default=".",
        help=f"Path to folder containing {YELLOW}foundry.toml{END} (default: current directory).",
    )
    parser.add_argument("--output", help="Path to save analysis results")

    def help_mode(description: str):
        if hide_dev_tool_help:
            return argparse.SUPPRESS
        else:
            return description

    parser.add_argument(
        "--debug",
        type=str,
        default=None,
        help=help_mode(
            'Send debug json to server. Can\'t use nested entries. Example: --debug \'{"admin": "true"}\' if you have admin privileges.'
        ),
    )

    parser.add_argument(
        "--local",
        action="store_true",
        help=help_mode("Run with local backend (http://localhost, port 5000)"),
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help=help_mode("Run with development backend (https://dev-server.hackbot.co, port 443)"),
    )

    parser.add_argument(
        "--skip-forge-build", action="store_true", help=help_mode("Skip forge build check")
    )


def add_learn_arguments(parser: argparse.ArgumentParser):
    """Add learn arguments to a parser."""
    parser.add_argument(
        "--auth-only", action="store_true", help="Only verify API key authentication"
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help=f"The URL provided by the user, to generate a {YELLOW}checklist.json{END} file, which is used to teach the hackbot about the types of vulnerabilities to look out for.",
    )
    parser.add_argument(
        "--merge", action="store_true", help="Merge the new checklist with the existing one"
    )
    parser.add_argument("--debug", type=str, default=None, help=argparse.SUPPRESS)


def add_api_key_argument(parser: argparse.ArgumentParser):
    """Add API key argument to a parser."""
    parser.add_argument(
        "--api-key",
        default=os.getenv("HACKBOT_API_KEY"),
        help=f"API key for authentication (default: {BLUE}HACKBOT_API_KEY{END} environment variable)",
    )


def setup_parser(
    hide_dev_tool_help: bool = True, return_run_parser: bool = False
) -> Union[argparse.ArgumentParser, tuple[argparse.ArgumentParser, argparse.ArgumentParser]]:
    """Parse the command line arguments."""
    description = (
        f"{RED}Hackbot{END} - ♨️ Kiss Solidity bugs Goodbye. "
        f"Visit {GREEN}https://hackbot.co{END} to get your API key and more information."
        f" Documentation: {GREEN}https://docs.hackbot.co{END}"
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-v", "--version", action="version", version=f"GatlingX Hackbot v{__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Description", required=True)

    # Create parsers for each command
    run_parser = subparsers.add_parser(
        Endpoint.RUN.value,
        help=f"{GREEN}Run analysis on foundry repository codebase. Require a `foundry.toml` file in the root of the repository{END}",
    )

    scope_parser = subparsers.add_parser(
        Endpoint.SCOPE.value,
        help=f"{GREY}Analyze the codebase and dump `scope.txt` file with the list of files that will be scanned in `hackbot run`{END}",
    )
    learn_parser = subparsers.add_parser(
        Endpoint.LEARN.value,
        help=f"{GREY}Analyze a link and generate a checklist.json file that can be used to teach the hackbot things to watch out for during `hackbot run` to improve the accuracy of the analysis{END}",
    )
    price_parser = subparsers.add_parser(
        Endpoint.PRICE.value,
        help=f"{GREY}Get the cost for running hackbot in your repo{END}",
    )
    report_parser = subparsers.add_parser(
        Endpoint.REPORT.value,
        help=f"{GREY}Generate a PDF report of bugs/POCs from a previous session{END}",
    )

    # Add API key to all command parsers that need it
    for cmd_parser in [run_parser, scope_parser, learn_parser, price_parser, report_parser]:
        cmd_parser.add_argument("-hh", "--hidden-help", action="store_true", help=argparse.SUPPRESS)

        add_api_key_argument(cmd_parser)

    for common_parser in [scope_parser, run_parser, price_parser, report_parser]:
        add_common_arguments(common_parser, hide_dev_tool_help=hide_dev_tool_help)

    add_learn_arguments(learn_parser)

    # Add session name argument for report command
    report_parser.add_argument(
        "session",
        type=str,
        help="Name of the session to generate report for",
    )

    run_parser.add_argument(
        "--checklist",
        type=str,
        required=False,
        help=f"A {YELLOW}checklist.json{END} file a list of issues the hackbot should pay further attention to, generated from {CYAN}hackbot learn --url <url>{END}",
    )

    run_parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Quiet mode, no interactive prompts",
    )

    if return_run_parser:
        return parser, run_parser
    return parser


def get_args() -> Union[argparse.Namespace, int]:
    """Parse the command line arguments."""
    parser = setup_parser(hide_dev_tool_help=True)
    assert isinstance(parser, argparse.ArgumentParser)
    args = parser.parse_args()

    if args.hidden_help:
        parsers = setup_parser(hide_dev_tool_help=False, return_run_parser=True)
        assert isinstance(parsers, tuple)
        parsers[1].print_help()
        return 0

    if args.command == Endpoint.RUN.value:
        ret = check_run_args(args)
    elif args.command == Endpoint.SCOPE.value:
        ret = check_scope_args(args)
    elif args.command == Endpoint.LEARN.value:
        ret = check_learn_args(args)
    elif args.command == Endpoint.PRICE.value:
        ret = check_price_args(args)
    elif args.command == Endpoint.REPORT.value:
        ret = check_report_args(args)
    else:
        raise ValueError(f"Invalid command: {args.command}")

    if isinstance(ret, int):
        return ret
    else:
        args = ret

    if args.local:
        log.info("Running in local server mode!")
        set_local_mode()
    elif args.dev:
        log.info("Running in development server mode!")
        set_dev_mode()

    return args


def check_common_args(args: argparse.Namespace) -> Union[argparse.Namespace, int]:
    """Check and validate commandline arguments for the run, scope and hack commands."""

    # Find closest enclosing path with foundry.toml by searching upwards
    # Check if given path contains foundry.toml
    source_path = Path(args.source).resolve()
    # Resolve fully (i.e. no .., no . etc)

    if source_path.exists() and (source_path / "foundry.toml").exists():
        args.source = source_path.absolute()
    else:
        log.error(f"❌ Error: No foundry.toml found in {source_path}!")
        return 1
    args.source = str(source_path.absolute())

    if not args.api_key:
        log.error(
            f"❌ Error: API key is required (either via --api-key or {BLUE}HACKBOT_API_KEY{END} environment variable)"
        )
        return 1

    try:
        if args.debug is not None:
            args.debug = json.loads(args.debug)
    except Exception:
        log.error(
            f"❌ Error: Invalid debug argument / JSON parse error on debug string: {args.debug}"
        )
        return 1

    return args


def check_scope_args(args: argparse.Namespace) -> Union[argparse.Namespace, int]:
    """Check and validate commandline arguments for the scope command."""
    return check_common_args(args)


def check_run_args(args: argparse.Namespace) -> Union[argparse.Namespace, int]:
    """Check and validate commandline arguments for the run command."""
    return check_common_args(args)


def check_learn_args(args: argparse.Namespace) -> Union[argparse.Namespace, int]:
    """Check and validate commandline arguments for the learn command."""
    if not args.url:
        log.error("❌ Error: URL is required for learn command")
        return 1

    if not args.api_key:
        log.error(
            "❌ Error: API key is required (either via --api-key or HACKBOT_API_KEY environment variable)"
        )
        return 1

    try:
        from urllib.parse import urlparse, ParseResult

        result: ParseResult = cast(ParseResult, urlparse(args.url))
        if not all([result.scheme, result.netloc]):
            log.error("❌ Error: Invalid URL format")
            return 1
    except Exception:
        log.error("❌ Error: Invalid URL")
        return 1

    if os.path.exists(Path.cwd() / "checklist.json"):
        if not args.merge:
            log.error("❌ Error: checklist.json already exists.")
            log.error("          - Either remove checklist.json and run hackbot learn again.")
            log.error(
                "          - Or run hackbot learn --merge to merge the new checklist with the existing one."
            )
            return 1
    else:
        if args.merge:
            log.error("❌ Error: No existing checklist.json found, cannot merge.")
            return 1

    return args


def check_price_args(_args: argparse.Namespace) -> Union[argparse.Namespace, int]:
    """Check and validate commandline arguments for the price command."""
    args = check_common_args(_args)
    if isinstance(args, int):
        return args

    return args


def check_report_args(args: argparse.Namespace) -> Union[argparse.Namespace, int]:
    """Check and validate commandline arguments for the report command."""
    if not args.api_key:
        log.error(
            f"❌ Error: API key is required (either via --api-key or {BLUE}HACKBOT_API_KEY{END} environment variable)"
        )
        return 1

    if not args.session:
        log.error("❌ Error: Session name is required")
        return 1

    return args


def learn_run(args: argparse.Namespace) -> int:
    """Run the learn command."""
    assert args.command == Endpoint.LEARN.value
    try:
        # Verify authentication
        auth_status = asyncio.run(authenticate(args.api_key))
        if auth_status is not None:
            log.error(
                f"❌ Authentication failed with error: {auth_status.message}. Please check your API key {BLUE}HACKBOT_API_KEY{RED} is set, and is valid. If you do not have an API key, please sign up at {GREEN}https://hackbot.co{RED} before running hackbot.${END}"
            )
            return 1

        log.info("✅ Authentication successful")

        if args.auth_only:
            return 0

        log.info(f"{BLUE}Starting analysis... Press {CYAN}Ctrl+C{BLUE} to cancel at any time{END}")

        asyncio.run(
            cli_learn(
                api_key=args.api_key,
                user_url=args.url,
                merge=args.merge,
            )
        )
    except Exception:
        log.error(f"❌ Error: {traceback.format_exc()}")
        return 1

    return 0


def get_bool_choice() -> bool:
    """Prompts the user to enter a yes or no response.
    Returns True if the user enters y, otherwise False."""
    while True:
        choice = input(f"\n{BLUE}Enter your choice [Y/n] (default: Y):{END} ").strip().lower()
        if choice and choice[0] in ["y", "n"]:
            return choice[0] == "y"
        elif choice == "":
            log.info("Going with default choice (Yes)")
            return True
        log.warning(
            "Please enter either a positive (starting with y) or negative (starting with n) response"
        )
    raise ValueError("Invalid point in program")


def handle_missing_scope_file() -> bool:
    """Prompts the user to let hackbot automatically generate scope.txt or manually change scope.txt.
    Returns whether the user wants hackbot to automatically generate scope.txt."""
    log.info(f"\n❌ No {RED}scope.txt{END} found in your project.")
    log.info("\nDo you want to let hackbot automatically generate scope.txt?")
    log.info(f"1) {GREY}Yes (let hackbot automatically generate scope.txt){END}")
    log.info(f"2) {GREY}No (manually change scope.txt{END}")

    choice = get_bool_choice()

    if not choice:
        log.info(f"\n{BLUE}📝 Next steps:{END}")
        log.info(f"1. Run {CYAN}hackbot scope{END} to generate scope.txt")
        log.info(f"2. Edit {CYAN}scope.txt{END} to customize which files to analyze")
        log.info(f"3. Run {CYAN}hackbot run{END} again to start analysis")
        return False
    else:
        return True


def ensure_scope_file(args: argparse.Namespace) -> bool:
    """Ensure that scope.txt exists."""
    scope_file = Path(args.source) / "scope.txt"
    if not scope_file.exists():
        auto_run = hasattr(args, "quiet") and args.quiet
        if auto_run or handle_missing_scope_file():
            log.info(
                f"No {RED}scope.txt{END} found in your project. Running {CYAN}hackbot scope{END} now to generate one..."
            )
            asyncio.run(
                cli_scope(
                    invocation_args={},
                    api_key=args.api_key,
                    source_path=args.source,
                    output=args.output,
                )
            )
            if not scope_file.exists():
                log.error(f"❌ Error: Failed to generate {RED}scope.txt{END}.")
                return False
            log.info("✅ Done generating scope.txt.")
        else:
            return False
    return True


def price_run(args: argparse.Namespace) -> int:
    """Run the price command.
    This also happens implicitly in hackbot run."""

    # Verify authentication
    auth_status = asyncio.run(authenticate(args.api_key))
    if auth_status is not None:
        log.error(
            f"❌ Authentication failed with error: {auth_status.message}. Please check your API key {BLUE}HACKBOT_API_KEY{RED} is set, and is valid. If you do not have an API key, please sign up at {GREEN}https://hackbot.co{RED} before running hackbot."
        )
        return 1

    log.info("✅ Authentication successful")

    if args.auth_only:
        return 0

    # Ensure scope.txt exists, same as in hackbot_run
    if not ensure_scope_file(args):
        log.error("❌ Error: No scope.txt. Exiting.")
        return 1

    # Get the pricing information
    results = asyncio.run(
        cli_price(
            api_key=args.api_key,
            source_path=args.source,
        )
    )

    # Output results to output-path
    if args.output and results:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)

    return 0


def confirm_price(args: argparse.Namespace) -> bool:
    """Confirm that the hackbot run, with the stated price."""
    # If --quiet, just proceed
    if hasattr(args, "quiet") and args.quiet:
        return True

    log.info(
        "Do you want to proceed with the run at the stated base fee price "
        "(you will not be charged additionally if we don't find high/medium severity vulnerabilities) "
        "according to https://docs.hackbot.co/docs/pricing?"
    )
    choice = get_bool_choice()
    if not choice:
        log.info("❌ Price confirmation failed. Exiting.")
        return False
    else:
        log.info("✅ Price confirmed. Proceeding with the run.")
        return True


def ensure_forge_build(args: argparse.Namespace) -> bool:
    """Ensure that normal `forge build` works locally."""
    if args.skip_forge_build:
        log.info("Skipping forge build check.")
        return True
    log.info(
        f"Running {GREEN}forge build{END} in source folder {args.source} to ensure it works locally..."
    )
    log.info(f"{GREY}----------   Output of forge build   ----------{END}")
    forge_build_works: int = subprocess.run(
        ["forge", "build"], check=False, cwd=args.source
    ).returncode
    log.info(f"{GREY}---------- End of forge build output ----------{END}")
    if forge_build_works != 0:
        log.info(f" Forge build returned non-zero exit code {forge_build_works}.")
        return False
    return True


def report_run(args: argparse.Namespace) -> int:
    """Run the report command."""
    try:
        # Verify authentication
        auth_result = asyncio.run(authenticate(args.api_key))
        if isinstance(auth_result, HackbotAuthError):
            log.error(f"❌ Error: {auth_result.message}")
            return 1

        if not args.session:
            log.error("❌ Error: Session name is required")
            return 1

        log.info(f"{BLUE}Generating report for session {args.session}...{END}")

        # Add invocation args setup
        invocation_args: Dict[str, str] = {"session_name": args.session}

        if args.debug is not None:
            log.info(f"Debug mode, sending (flat, since only using http forms): {args.debug}")
            for key, value in args.debug.items():
                invocation_args[key] = value

        # Generate the report
        results = asyncio.run(
            cli_report(
                api_key=args.api_key,
                invocation_args=invocation_args,
                output=args.output,
            )
        )

        # Output results to output-path
        if args.output and results:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)

        return 0

    except KeyboardInterrupt:
        log.info("\n❌ Report generation cancelled by user")
        return 1
    except Exception:
        log.error(f"❌ Error: {traceback.format_exc()}")
        return 1


def hackbot_run(args: argparse.Namespace) -> int:
    """Run the hackbot tool."""

    # Ensure normal `forge build` works locally.
    forge_build_works: bool = ensure_forge_build(args)
    if not forge_build_works:
        log.error("❌ Error: Forge build failed. Exiting.")
        return 1

    price_ret = price_run(args)
    if price_ret != 0:
        log.error("❌ Error: Price run failed. Exiting.")
        return price_ret

    # Confirm that the hackbot run, with the stated price.
    if not confirm_price(args):
        return 1

    try:
        # Add invocation args setup
        invocation_args: Dict[str, str] = {}

        if args.debug is not None:
            log.info(f"Debug mode, sending (flat, since only using http forms): {args.debug}")
            for key, value in args.debug.items():
                invocation_args[key] = value

        log.info(f"{BLUE}Starting analysis... Press {CYAN}Ctrl+C{BLUE} to cancel at any time{END}")
        # The only values of command that can be here are run and scope
        if args.command == Endpoint.RUN.value:
            # Perform the bug analysis
            results = asyncio.run(
                cli_run(
                    invocation_args=invocation_args,
                    api_key=args.api_key,
                    source_path=args.source,
                    output=args.output,
                    checklist=args.checklist,
                )
            )

        elif args.command == Endpoint.SCOPE.value:
            # Perform the scope analysis
            results = asyncio.run(
                cli_scope(
                    invocation_args=invocation_args,
                    api_key=args.api_key,
                    source_path=args.source,
                    output=args.output,
                )
            )
        else:
            log.error(f"❌ Error: Invalid command: {args.command}")
            return 1

        # Output results to output-path
        if args.output and results:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)

        return 0

    except ClientPayloadError:
        log.error(
            "❌ The server terminated the connection prematurely, most likely due to an error in the scanning process. Check the streamed logs for error messages. Support: support@gatlingx.com"
        )
        return 1
    except Exception as e:
        if str(e) == "Hack request failed: 413":
            log.error(
                "❌ The source code directory is too large to be scanned. Must be less than 256MB."
            )
            return 1
        else:
            raise e
