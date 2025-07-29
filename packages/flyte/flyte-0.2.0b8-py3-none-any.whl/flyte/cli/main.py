import rich_click as click

from flyte._logging import initialize_logger, logger

from ._abort import abort
from ._common import CLIConfig
from ._create import create
from ._deploy import deploy
from ._gen import gen
from ._get import get
from ._run import run

click.rich_click.COMMAND_GROUPS = {
    "flyte": [
        {
            "name": "Running Workflows",
            "commands": ["run", "abort"],
        },
        {
            "name": "Management",
            "commands": ["create", "deploy", "get"],
        },
        {
            "name": "Documentation Generation",
            "commands": ["gen"],
        },
    ]
}

help_config = click.RichHelpConfiguration(
    use_markdown=True,
    use_markdown_emoji=True,
)


def _verbosity_to_loglevel(verbosity: int) -> int | None:
    """
    Converts a verbosity level from the CLI to a logging level.

    :param verbosity: verbosity level from the CLI
    :return: logging level
    """
    import logging

    match verbosity:
        case 0:
            return None
        case 1:
            return logging.WARNING
        case 2:
            return logging.INFO
        case _:
            return logging.DEBUG


@click.group(cls=click.RichGroup)
@click.option(
    "--endpoint",
    type=str,
    required=False,
    help="The endpoint to connect to, this will override any config and simply used pkce to connect.",
)
@click.option(
    "--insecure/--secure",
    is_flag=True,
    required=False,
    help="Use insecure connection to the endpoint. If secure is specified, the CLI will use TLS.",
    type=bool,
    default=None,
    show_default=True,
)
@click.option(
    "-v",
    "--verbose",
    required=False,
    help="Show verbose messages and exception traces, multiple times increases verbosity (e.g., -vvv).",
    count=True,
    default=0,
    type=int,
)
@click.option(
    "--org",
    type=str,
    required=False,
    help="Organization to use",
)
@click.option(
    "-c",
    "--config",
    "config_file",
    required=False,
    type=click.Path(exists=True),
    help="Path to config file (YAML format) to use for the CLI. If not specified,"
    " the default config file will be used.",
)
@click.rich_config(help_config=help_config)
@click.pass_context
def main(
    ctx: click.Context,
    endpoint: str | None,
    insecure: bool,
    verbose: int,
    org: str | None,
    config_file: str | None,
):
    """
    ### Flyte entrypoint for the CLI
    The Flyte CLI is a command line interface for interacting with Flyte.

    The flyte cli follows a simple verb based structure, where the top-level commands are verbs that describe the action
    to be taken, and the subcommands are nouns that describe the object of the action.

    The root command can be used to configure the CLI for most commands, such as setting the endpoint,
     organization, and verbosity level.

     Example: Set endpoint and organization
     ```bash
      flyte --endpoint <endpoint> --org <org> get project <project_name>
     ```

     Example: Increase verbosity level (This is useful for debugging, this will show more logs and exception traces)
      ```bash
      flyte -vvv get logs <run-name>
      ```

      Example: Override the default config file
    ```bash
    flyte --config /path/to/config.yaml run ...
    ```

    👉 [Documentation](https://www.union.ai/docs/flyte/user-guide/) \n
    👉 [GitHub](https://github.com/flyteorg/flyte) - Please leave a ⭐. \n
    👉 [Slack](https://slack.flyte.org) - Join the community and ask questions.
    👉 [Issues](https://github.com/flyteorg/flyte/issues)

    """
    import flyte.config as config

    log_level = _verbosity_to_loglevel(verbose)
    if log_level is not None:
        initialize_logger(log_level)

    cfg = config.auto(config_file=config_file)
    logger.debug(f"Using config file discovered at location {cfg.source}")

    final_insecure = cfg.platform.insecure
    if insecure is not None:
        final_insecure = insecure

    ctx.obj = CLIConfig(
        log_level=log_level,
        endpoint=endpoint or cfg.platform.endpoint,
        insecure=final_insecure,
        org_override=org or cfg.task.org,
        config=cfg,
        ctx=ctx,
    )
    logger.debug(f"Final materialized Cli config: {ctx.obj}")


main.add_command(run)
main.add_command(deploy)
main.add_command(get)  # type: ignore
main.add_command(create)  # type: ignore
main.add_command(abort)  # type: ignore
main.add_command(gen)  # type: ignore
