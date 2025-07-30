import click
import readline

class InteractiveGroup(click.Group):
    def invoke(self, ctx):
        if not ctx.invoked_subcommand:
            self.interactive(ctx)
        else:
            super().invoke(ctx)

    def interactive(self, ctx):
        click.echo("🌀 Interactive CLI Mode. Type 'help' for commands. Type 'exit' to quit.\n")

        readline.set_completer(self.make_completer())
        readline.parse_and_bind("tab: complete")
        readline.set_history_length(1000)

        while True:
            try:
                user_input = input(f"{ctx.command.name}> ").strip()
                if user_input.lower() in ("exit", "quit"):
                    click.echo("👋 Exiting CLI. Goodbye!")
                    break
                elif user_input == "help":
                    click.echo("Available commands:")
                    for cmd in self.list_commands(ctx):
                        click.echo(f"  {cmd}")
                    continue
                elif not user_input:
                    continue

                # Run subcommand
                args = user_input.split()
                # This must NOT invoke the current command group without subcommand
                sub_cmd = args[0]
                if sub_cmd not in self.commands:
                    click.echo(f"❌ Unknown command: {sub_cmd}")
                    continue

                self.commands[sub_cmd].main(
                    args=args[1:],  # exclude the subcommand name
                    prog_name=f"{ctx.command.name} {sub_cmd}",
                    standalone_mode=False
                )

            except click.ClickException as ce:
                ce.show()
            except Exception as e:
                click.echo(f"Error: {e}")
            except KeyboardInterrupt:
                click.echo("\nInterrupted. Type 'exit' to quit.")

    def make_completer(self):
        commands = self.list_commands(None)
        def completer(text, state):
            matches = [cmd for cmd in commands if cmd.startswith(text)]
            return matches[state] if state < len(matches) else None
        return completer
