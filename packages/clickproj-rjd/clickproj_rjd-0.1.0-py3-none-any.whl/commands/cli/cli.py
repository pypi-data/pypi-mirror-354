import click

from commands.interactive_group import InteractiveGroup
from commands.cli.greet.greet import greet
from commands.cli.user.user import user


@click.group(name = "cli", cls = InteractiveGroup,invoke_without_command = True)
@click.option("--debug", is_flag=True, default=False)
@click.pass_context
def cli(ctx, debug):

    """Main cli entrypoint"""
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    if debug:
        click.echo("[DEBUG] Debug mode is ON")

# Registering commands
cli.add_command(greet)
cli.add_command(user)

def main():
    """Entry point for the application"""
    return cli(standalone_mode=True)

if __name__ == "__main__":
    main()