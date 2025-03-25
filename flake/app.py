import typer
import json
import sys
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

def handleException(e: Exception, debug: bool = False):
    if debug:
        raise e
    print(e, file=sys.stderr)
    sys.exit(1)

@app.command()
def ui(url: str = default_url):
    """Start the Flake dashboard"""
    #typer.echo("UI command")
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
           pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
           debug: bool = typer.Option(False, help="Print detailed error")):
    """Get the status of the scheduler"""
    try:
        printJson(SchedulerView(url).get_status(), pretty)
    except Exception as e:
        handleException(e, debug)
    
@app.command()
def start(url: str = default_url,
          pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
          debug: bool = typer.Option(False, help="Print detailed error")):
    """Start the scheduler"""
    try:
        printJson(SchedulerView(url).start(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def stop(url: str = default_url,
         pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
         debug: bool = typer.Option(False, help="Print detailed error")):
    """Stop the scheduler"""
    try:
        printJson(SchedulerView(url).stop(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def restart(url: str = default_url,
            pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
            debug: bool = typer.Option(False, help="Print detailed error")):
    """Restart the scheduler"""
    try:
        printJson(SchedulerView(url).restart(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def pause(url: str = default_url,
          pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
          debug: bool = typer.Option(False, help="Print detailed error")):
    """Pause the scheduler"""
    try:
        printJson(SchedulerView(url).pause(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def resume(url: str = default_url,
           pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
           debug: bool = typer.Option(False, help="Print detailed error")):
    """Resume the scheduler"""
    try:
        printJson(SchedulerView(url).resume(), pretty)
    except Exception as e:
        handleException(e, debug)

# Job commands

@app.command()
def jobs(url: str = default_url,
         instrument: Optional[str] = typer.Option(None, help="Filter jobs by instrument"),
         pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
         debug: bool = typer.Option(False, help="Print detailed error")):
    """Get all jobs in the scheduler"""
    try:
        printJson(SchedulerView(url).get_jobs(instrument), pretty)
    except Exception as e:
        handleException(e, debug)
        
    
@app.command()
def job(url: str = default_url,
        id: str = typer.Argument(help="The ID of the job"), 
        pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
        debug: bool = typer.Option(False, help="Print detailed error")):
    """Get a scheduler's job"""
    try:
        printJson(JobView(url, id).get(), pretty)
    except Exception as e:
        handleException(e, debug)
    
@app.command()
def job_status(url: str = default_url,
               id: str = typer.Argument(help="The ID of the job"),
               pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
               debug: bool = typer.Option(False, help="Print detailed error")):
    """Get the status of a scheduler's job"""
    try:
        printJson(JobView(url, id).get_status(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def job_start(url: str = default_url,
              id: str = typer.Argument(help="The ID of the job"),
              pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
              debug: bool = typer.Option(False, help="Print detailed error")):
    """Start a scheduler's job"""
    try:
        printJson(JobView(url, id).start(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def job_stop(url: str = default_url,
             id: str = typer.Argument(help="The ID of the job"),
             pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
             debug: bool = typer.Option(False, help="Print detailed error")):
    """Stop a scheduler's job"""
    try:
        printJson(JobView(url, id).stop(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def job_restart(url: str = default_url,
                id: str = typer.Argument(help="The ID of the job"),
                pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
                debug: bool = typer.Option(False, help="Print detailed error")):
    """Restart a scheduler's job"""
    try:
        printJson(JobView(url, id).restart(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def job_pause(url: str = default_url,
              id: str = typer.Argument(help="The ID of the job"),
              pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
              debug: bool = typer.Option(False, help="Print detailed error")):
    """Pause a scheduler's job"""
    try:
        printJson(JobView(url, id).pause(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def job_resume(url: str = default_url,
               id: str = typer.Argument(help="The ID of the job"),
               pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
               debug: bool = typer.Option(False, help="Print detailed error")):
    """Resume a scheduler's job"""
    try:
        printJson(JobView(url, id).resume(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def job_run(url: str = default_url,
                id: str = typer.Argument(help="The ID of the job"),
                pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
                debug: bool = typer.Option(False, help="Print detailed error")):
    """Trigger a scheduler's job one-time immediate execution (works even if job is paused)"""
    try:
        printJson(JobView(url, id).run(), pretty)
    except Exception as e:
        handleException(e, debug)

# Config commands

@app.command()
def config_reload(url: str = default_url,
                  pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
                  debug: bool = typer.Option(False, help="Print detailed error")):
    """Reload configuration, update the scheduler jobs accordingly"""
    try:
        printJson(ConfigView(url).reload(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def settings(url: str = default_url,
                pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
                debug: bool = typer.Option(False, help="Print detailed error")):
    """Get settings configuration"""
    try:
        printJson(ConfigView(url).get_settings(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def runtime(url: str = default_url,
                pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
                debug: bool = typer.Option(False, help="Print detailed error")):
    """Get runtime information"""
    try:
        printJson(ConfigView(url).get_runtime(), pretty)
    except Exception as e:
        handleException(e, debug)

# Instrument commands

@app.command()
def instruments(url: str = default_url,
                pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
                debug: bool = typer.Option(False, help="Print detailed error")):
    """Get all instrument configurations"""
    try:
        printJson(ConfigView(url).get_instruments(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def instrument(url: str = default_url,
               name: str = typer.Argument(help="The name of the instrument"),
               pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
               debug: bool = typer.Option(False, help="Print detailed error")):
    """Get an instrument configuration"""
    try:
        printJson(InstrumentView(url, name).get(), pretty)
    except Exception as e:
        handleException(e, debug)

@app.command()
def instrument_logs(url: str = default_url,
               name: str = typer.Argument(help="The name of the instrument"),
               tail: int = typer.Option(100, help="Number of the last log lines to retrieve, all lines if not positive", show_default=True),
               debug: bool = typer.Option(False, help="Print detailed error")):
    """Get the instrument logs"""
    try:
        for line in InstrumentView(url, name).get_log_lines(tail):
            print(line)
    except Exception as e:
        handleException(e, debug)
        
@app.command()
def instrument_log_files(url: str = default_url,
               name: str = typer.Argument(help="The name of the instrument"),
               file: str = typer.Option("", help="The path to the zip file to write, default is <name.zip> in the current working directory", show_default=True),
               debug: bool = typer.Option(False, help="Print detailed error")):
    """Get the instrument log files in a zip"""
    try:
        zip_file = file if file else f"{name}.zip"
        with open(zip_file, "wb") as file:
            for chunk in InstrumentView(url, name).get_log_stream():
                file.write(chunk)
    except Exception as e:
        handleException(e, debug)

@app.command()
def instrument_remove(url: str = default_url,
               name: str = typer.Argument(help="The name of the instrument"),
               pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
               debug: bool = typer.Option(False, help="Print detailed error")):
    """Remove an instrument from configuration"""
    try:
        printJson(InstrumentView(url, name).remove(), pretty)
    except Exception as e:
        handleException(e, debug)

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
                      pretty: bool = typer.Option(False, help="Pretty print the JSON output"),
                      debug: bool = typer.Option(False, help="Print detailed error")):
    """Add or update an instrument configuration"""
    data = None
            
    # From JSON file
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
    
    try:
        printJson(ConfigView(url).add_or_update_instrument(data), pretty)
    except Exception as e:
        handleException(e, debug)

def main() -> None:
    """The main function of the application

    Used by the poetry entrypoint.
    """

    basicConfig(level=INFO)
    app()


if __name__ == "__main__":
    main()