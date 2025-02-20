import typer
from logging import INFO, basicConfig, info, warning, error
from .views.ui import ttk, FlakeUI, theme_name
from .views.scheduler import SchedulerView

# Initialise the Typer class
app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    pretty_exceptions_show_locals=False,
)

default_url = "http://127.0.0.1:8000"

@app.command()
def ui(url: str = default_url):
    typer.echo("UI command")
    app = ttk.Window(
        title="Flake", 
        themename=theme_name, 
        resizable=(False, False)
    )
    FlakeUI(app, url=url)
    app.mainloop()

@app.command()
def status(url: str = default_url):
    print(SchedulerView(url).get_status())

@app.command()
def start(url: str = default_url):
    print(SchedulerView(url).start())

@app.command()
def stop(url: str = default_url):
    print(SchedulerView(url).stop())

@app.command()
def restart(url: str = default_url):
    print(SchedulerView(url).restart())

@app.command()
def pause(url: str = default_url):
    print(SchedulerView(url).pause())

@app.command()
def resume(url: str = default_url):
    print(SchedulerView(url).resume())

def main() -> None:
    """The main function of the application

    Used by the poetry entrypoint.
    """

    basicConfig(level=INFO)
    app()


if __name__ == "__main__":
    main()