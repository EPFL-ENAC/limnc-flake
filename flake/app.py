import typer
import json
from typing import Optional
from pathlib import Path
from logging import INFO, basicConfig, info, warning, error
from .views.ui import ttk, FlakeUI, theme_name
from .views.scheduler import SchedulerView
from .views.job import JobView
from .views.config import ConfigView
from .views.instrument import InstrumentView

# Initialise the Typer class
app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    pretty_exceptions_show_locals=False,
)

default_url = "http://127.0.0.1:8000"

def printJson(data: dict, pretty: bool = True):
    if pretty:
        print(json.dumps(data, indent=2))
    else:
        print(json.dumps(data))

@app.command()
def ui(url: str = default_url):
    """Start the Flake dashboard"""
    typer.echo("UI command")
    app = ttk.Window(
        title="Flake", 
        themename=theme_name, 
        resizable=(False, False)
    )
    FlakeUI(app, url=url)
    app.mainloop()

# Scheduler commands

@app.command()
def status(url: str = default_url,
           pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Get the status of the scheduler"""
    printJson(SchedulerView(url).get_status(), pretty)

@app.command()
def start(url: str = default_url,
          pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Start the scheduler"""
    printJson(SchedulerView(url).start(), pretty)

@app.command()
def stop(url: str = default_url,
         pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Stop the scheduler"""
    printJson(SchedulerView(url).stop(), pretty)

@app.command()
def restart(url: str = default_url,
            pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Restart the scheduler"""
    printJson(SchedulerView(url).restart(), pretty)

@app.command()
def pause(url: str = default_url,
          pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Pause the scheduler"""
    printJson(SchedulerView(url).pause(), pretty)

@app.command()
def resume(url: str = default_url,
           pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Resume the scheduler"""
    printJson(SchedulerView(url).resume(), pretty)
    
# Job commands

@app.command()
def jobs(url: str = default_url,
         pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Get all jobs in the scheduler"""
    printJson(SchedulerView(url).get_jobs(), pretty)
    
@app.command()
def job(url: str = default_url,
        id: str = typer.Argument(help="The ID of the job"), 
        pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Get a scheduler's job"""
    printJson(JobView(url, id).get(), pretty)
    
@app.command()
def job_status(url: str = default_url,
               id: str = typer.Argument(help="The ID of the job"),
               pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Get the status of a scheduler's job"""
    printJson(JobView(url, id).get_status(), pretty)

@app.command()
def job_start(url: str = default_url,
              id: str = typer.Argument(help="The ID of the job"),
              pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Start a scheduler's job"""
    printJson(JobView(url, id).start(), pretty)

@app.command()
def job_stop(url: str = default_url,
             id: str = typer.Argument(help="The ID of the job"),
             pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Stop a scheduler's job"""
    printJson(JobView(url, id).stop(), pretty)

@app.command()
def job_restart(url: str = default_url,
                id: str = typer.Argument(help="The ID of the job"),
                pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Restart a scheduler's job"""
    printJson(JobView(url, id).restart(), pretty)

@app.command()
def job_pause(url: str = default_url,
              id: str = typer.Argument(help="The ID of the job"),
              pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Pause a scheduler's job"""
    printJson(JobView(url, id).pause(), pretty)

@app.command()
def job_resume(url: str = default_url,
               id: str = typer.Argument(help="The ID of the job"),
               pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Resume a scheduler's job"""
    printJson(JobView(url, id).resume(), pretty)
    
# Instrument commands

@app.command()
def instruments(url: str = default_url,
                pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Get all instrument configurations"""
    printJson(ConfigView(url).get_instruments(), pretty)

@app.command()
def instrument(url: str = default_url,
               id: str = typer.Argument(help="The ID of the instrument"),
               pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Get an instrument configuration"""
    printJson(InstrumentView(url, id).get(), pretty)

@app.command()
def instrument_remove(url: str = default_url,
               id: str = typer.Argument(help="The ID of the instrument"),
               pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Remove an instrument from configuration"""
    printJson(InstrumentView(url, id).remove(), pretty)
    
@app.command()
def instrument_update(url: str = default_url,
                      json_file: Optional[Path] = typer.Option(
                        None,
                        "--file", "-f",
                        help="Instrument configuration as a JSON file",
                        exists=True,
                        readable=True,
                        dir_okay=False),
                      json_text: Optional[str] = typer.Option(
                        None,
                        "--json", "-j",
                        help="Instrument configuration as a JSON string",
                      ),
                      pretty: bool = typer.Option(False, help="Pretty print the JSON output")):
    """Add or update an instrument configuration"""
    data = None
    
    # Method 1: From file
    if json_file:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            typer.echo(f"Error: {json_file} contains invalid JSON", err=True)
            raise typer.Exit(code=1)
    
    # Method 2: From text parameter
    elif json_text:
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            typer.echo("Error: Invalid JSON string provided", err=True)
            raise typer.Exit(code=1)
    
    if data is None:
        typer.echo("Error: No JSON data provided", err=True)
        raise typer.Exit(code=1)
    
    printJson(ConfigView(url).add_or_update_instrument(data), pretty)


def main() -> None:
    """The main function of the application

    Used by the poetry entrypoint.
    """

    basicConfig(level=INFO)
    app()


if __name__ == "__main__":
    main()