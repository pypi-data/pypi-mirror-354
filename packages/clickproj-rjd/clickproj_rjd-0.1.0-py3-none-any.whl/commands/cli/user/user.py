import click

@click.group()
@click.pass_context
def user(ctx):
    """User related operations"""
    if(ctx.obj.get('DEBUG')):

        click.echo("[DEBUG] User group command initialized")

@user.command(help = "Create a new user")
@click.argument("username")
@click.option("--admin", is_flag = True, help = "Make the user an admin")
@click.pass_context
def add(ctx, username, admin):
    """Add a new user"""
    role = "ADMIN" if admin else "REGULAR USER"
    if ctx.obj.get('DEBUG'):
        click.echo(f"[DEBUG] Adding User {username} as role {role}...")
    click.echo(f"✅ Added user '{username}' with role: {role}")

@user.command(help = "Remove a user")
@click.argument("username")
@click.pass_context
def delete(ctx, username):
    """Delete a user"""
    if(ctx.obj.get('DEBUG')):
        click.echo(f"[DEBUG] Deleting User {username}...")
    click.echo(f"User {username} deleted...")


