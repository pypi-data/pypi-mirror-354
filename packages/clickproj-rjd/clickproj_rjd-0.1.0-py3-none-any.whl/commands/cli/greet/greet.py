import click

@click.command()
@click.argument('name')
@click.pass_context
def greet(ctx, name):
    """Greet someone"""
    if ctx.obj.get('DEBUG'):
        click.echo(f"👋 [DEBUG] Greeting {name}...")
    print(name)

    click.echo(f"👋 Hello, {name}!")
