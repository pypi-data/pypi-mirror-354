from pathlib import Path
from typing import get_args

import rich_click as click

import flyte.cli._common as common
from flyte.remote._secret import SecretTypes


@click.group(name="create")
def create():
    """
    The create subcommand allows you to create resources in a Flyte deployment.
    """


@create.command(cls=common.CommandBase)
@click.argument("name", type=str, required=True)
@click.argument("value", type=str, required=False)
@click.option("--from-file", type=click.Path(exists=True), help="Path to the file with the binary secret.")
@click.option(
    "--type", type=click.Choice(get_args(SecretTypes)), default="regular", help="Type of the secret.", show_default=True
)
@click.pass_obj
def secret(
    cfg: common.CLIConfig,
    name: str,
    value: str | bytes | None = None,
    from_file: str | None = None,
    type: SecretTypes = "regular",
    project: str | None = None,
    domain: str | None = None,
):
    """
    Create a new secret, the name of the secret is required.

    Examples:
    ```bash
    flyte create secret my_secret --value my_value
    ```
    If `--from-file` is specified, the value will be read from the file instead of being provided directly.
    Example:
    ```bash
    flyte create secret my_secret --from-file /path/to/secret_file
    ```
    Secret types can be used to create specific types of secrets. Some secrets are useful for image pull, while some
    are `regular` / general purpose secrets.
    Example:
    ```bash
    flyte create secret my_secret --type image_pull
    ```
    """
    from flyte.remote import Secret

    cfg.init(project, domain)
    if from_file:
        with open(from_file, "rb") as f:
            value = f.read()
    Secret.create(name=name, value=value, type=type)


@create.command(cls=common.CommandBase)
@click.option("--endpoint", type=str, help="Endpoint of the Flyte backend.")
@click.option("--insecure", is_flag=True, help="Use insecure connection to the Flyte backend.")
@click.option(
    "--org",
    type=str,
    required=False,
    help="Organization to use, this will override the organization in the config file.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=False, writable=True),
    default=Path.cwd() / "config.yaml",
    help="Path to the output dir where the config will be saved, defaults to current directory.",
    show_default=True,
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Force overwrite the config file if it already exists.",
    show_default=True,
    prompt="Are you sure you want to overwrite the config file?",
    confirmation_prompt=True,
)
def config(
    output: Path,
    endpoint: str | None = None,
    insecure: bool = False,
    org: str | None = None,
    project: str | None = None,
    domain: str | None = None,
    force: bool = False,
):
    """
    This command creates a configuration file for Flyte CLI.
    If the `--output` option is not specified, it will create a file named `config.yaml` in the current directory.
    If the file already exists, it will raise an error unless the `--force` option is used.
    """
    import yaml

    if output.exists() and not force:
        raise click.BadParameter(f"Output file {output} already exists. Use --force to overwrite.")

    with open(output, "w") as f:
        d = {
            "admin": {
                "endpoint": endpoint,
                "insecure": insecure,
            },
            "task": {
                "org": org,
                "project": project,
                "domain": domain,
            },
        }
        yaml.dump(d, f)

    click.echo(f"Config file created at {output}")
