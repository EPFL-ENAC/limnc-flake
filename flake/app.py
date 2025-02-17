import typer
from logging import INFO, basicConfig, info, warning, error
from flake.services.scheduler import start

# Initialise the Typer class
app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    pretty_exceptions_show_locals=False,
)


@app.command()
def config():
    typer.echo("Config command")
    

@app.command()
def scheduler():
    typer.echo("Scheduler command")
    start()
    
def main() -> None:
    """The main function of the application

    Used by the poetry entrypoint.
    """

    basicConfig(level=INFO)
    app()


if __name__ == "__main__":
    main()