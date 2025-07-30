import os
import subprocess
import yaml
import json
import click
import sys

# Ensure 'echoshell' is importable when running from source
try:
    from echoshell.redis_connector import RedisConnector
except ModuleNotFoundError:
    src_path = os.path.join(os.path.dirname(__file__), "src")
    if os.path.isdir(src_path) and src_path not in sys.path:
        sys.path.insert(0, src_path)
    from echoshell.redis_connector import RedisConnector

from LoreWeave.parser import LoreWeaveParser

@click.group()
def cli():
    """LoreWeave CLI for narrative processing and storage."""
    pass

@click.command()
def init():
    """Initialize LoreWeave configuration and directories."""
    repo_path = os.getcwd()
    config_path = os.path.join(repo_path, "LoreWeave", "config.yaml")
    intention_results_dir = os.path.join(repo_path, "LoreWeave", "intention_results")
    narrative_results_dir = os.path.join(repo_path, "LoreWeave", "narrative_results")
    commit_results_dir = os.path.join(repo_path, "LoreWeave", "commit_results")
    github_issues_dir = os.path.join(repo_path, "LoreWeave", "github_issues")

    os.makedirs(intention_results_dir, exist_ok=True)
    os.makedirs(narrative_results_dir, exist_ok=True)
    os.makedirs(commit_results_dir, exist_ok=True)
    os.makedirs(github_issues_dir, exist_ok=True)

    default_config = {
        "version": "0.1",
        "parser": {
            "glyph_patterns": [
                r"Glyph: ([\w\s]+) \(([^)]+)\)",
                r"([🌀🪶❄️🧩🧠🌸]) ([\w\s]+)"
            ]
        }
    }

    with open(config_path, "w") as f:
        yaml.dump(default_config, f)

    click.echo("LoreWeave initialized with default configuration and directories.")

@click.command(help="Execute narrative hooks, sync GitHub issues and refresh the RedStone registry")
@click.option('--verbose', is_flag=True, help='Enable verbose output for each processing step.')
def run(verbose):
    """Run LoreWeave narrative processing and storage.

    This command performs the following actions:
    1. Post-commit parsing to produce plot points and white feather moments.
    2. Post-push parsing to build narrative fragments.
    3. GitHub issue synchronization, writing a summary under `LoreWeave/github_issues/`.
    4. RedStone registry refresh to keep local metadata current.
    Parsed fragments are stored in Redis for later retrieval.
    """
    repo_path = os.getcwd()
    config_path = os.path.join(repo_path, "LoreWeave", "config.yaml")
    parser = LoreWeaveParser(repo_path, config_path)

    # Run post-commit processing
    if verbose:
        click.echo('Running post-commit processing...')
    parser.run_post_commit()

    # Run post-push processing
    if verbose:
        click.echo('Running post-push processing...')
    parser.run_post_push()

    # Sync with GitHub issues
    if verbose:
        click.echo('Syncing with GitHub issues...')
    parser.sync_with_github_issues()

    # Update RedStone registry
    if verbose:
        click.echo('Updating RedStone registry...')
    parser.update_redstone_registry()

    # Process and store narrative fragments in Redis
    if verbose:
        click.echo('Storing narrative fragments in Redis...')
    redis_conn = RedisConnector()
    commit_messages = parser.parse_commit_messages_since_last_push()
    for commit in commit_messages:
        parsed_data = parser.parse_commit_message(commit["message"])
        redis_conn.set_key(f"narrative_fragment:{commit['commit_hash']}", json.dumps(parsed_data))

@click.command()
def help():
    """Show detailed help for LoreWeave commands."""
    click.echo(cli.get_help(click.Context(cli)))

# Add commands to the CLI group
cli.add_command(init)
cli.add_command(run)
cli.add_command(help)

if __name__ == "__main__":
    cli()
