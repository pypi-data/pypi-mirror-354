"""
# CLI for Flyte

The flyte cli follows a simple verb based structure, where the top-level commands are verbs that describe the action
to be taken, and the subcommands are nouns that describe the object of the action.
"""

from flyte.cli.main import main

__all__ = ["main"]
