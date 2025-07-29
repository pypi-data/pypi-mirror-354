"""
# Utilities based on `click` for the CLI framework.
"""

from collections.abc import Iterable

import click


class AliasedGroup(click.Group):
    """
    Custom click group that allows commands to have multiple aliases.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._alias_map: dict[str, str] = {}

    def add_command(self, cmd, name=None):
        # Get all names (primary + aliases)
        if name and isinstance(name, str):
            names = (name,)
        elif name and isinstance(name, Iterable):
            names = tuple(name)
        elif cmd.name and isinstance(cmd.name, str):
            names = (cmd.name,)
        elif cmd.name and isinstance(cmd.name, Iterable):
            names = tuple(cmd.name)
        else:
            names = (cmd.callback.__name__,)

        # Set the primary name (the first one)
        primary = names[0] if name is None else name
        cmd.name = primary
        super().add_command(cmd, primary)

        # Register aliases
        for alias in names[1:]:
            self._alias_map[alias] = primary

    def get_command(self, ctx, cmd_name) -> click.Command | None:
        # Resolve aliases
        if cmd_name in self._alias_map:
            cmd_name = self._alias_map[cmd_name]

        # Fetch the command
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        return None

    def resolve_command(self, ctx, args) -> tuple[str | None, click.Command | None, list[str]]:
        # Resolve alias before handing off
        if args:
            first = args[0]
            if first in self._alias_map:
                args[0] = self._alias_map[first]
        return super().resolve_command(ctx, args)
