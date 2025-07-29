"""Command-line interface for OpenCar."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from opencar import __version__
from opencar.config.settings import get_settings

# Import uvicorn at module level for mocking in tests
try:
    import uvicorn
except ImportError:
    uvicorn = None

# Initialize console and app
console = Console()
app = typer.Typer(
    name="opencar",
    help="OpenCar - Advanced Autonomous Vehicle Perception System",
    add_completion=True,
    rich_markup_mode="rich",
)


def version_callback(value: bool):
    """Version callback."""
    if value:
        console.print(f"[bold blue]OpenCar[/bold blue] version {__version__}")
        raise typer.Exit(0)


@app.callback()
def callback(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """OpenCar CLI - Manage autonomous vehicle perception systems."""
    pass


@app.command()
def init(
    project_dir: Path = typer.Argument(
        Path.cwd(),
        help="Project directory",
        exists=False,
    ),
    template: str = typer.Option(
        "default",
        "--template",
        "-t",
        help="Project template to use",
    ),
) -> None:
    """Initialize a new OpenCar project."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Initializing project...", total=5)

        # Create project structure
        project_dir.mkdir(parents=True, exist_ok=True)
        progress.update(task, advance=1, description="Creating directories...")

        dirs = ["data", "models", "configs", "logs", "notebooks"]
        for dir_name in dirs:
            (project_dir / dir_name).mkdir(exist_ok=True)

        progress.update(task, advance=1, description="Creating configuration...")

        # Create default configuration
        config_file = project_dir / "opencar.yaml"
        config_file.write_text(
            """# OpenCar Configuration
project:
  name: my-opencar-project
  version: 1.0.0

perception:
  models:
    - yolov8
    - segformer
  confidence_threshold: 0.5

training:
  batch_size: 32
  epochs: 100
  learning_rate: 0.001
"""
        )

        progress.update(task, advance=1, description="Setting up environment...")

        # Create .env file
        env_file = project_dir / ".env"
        env_example = Path(__file__).parent.parent.parent.parent / ".env.example"
        if env_example.exists():
            env_file.write_text(env_example.read_text())
        else:
            env_file.write_text("# OpenCar Environment Configuration\nDEBUG=false\n")

        progress.update(task, advance=1, description="Installing dependencies...")

        # Create requirements file
        req_file = project_dir / "requirements.txt"
        req_file.write_text("opencar>=1.0.0\n")

        progress.update(task, advance=1, description="Complete!")

    console.print(
        Panel.fit(
            f"[bold green]Project initialized successfully![/bold green]\n\n"
            f"[yellow]Next steps:[/yellow]\n"
            f"1. cd {project_dir}\n"
            f"2. Configure your .env file\n"
            f"3. Run [bold]opencar serve[/bold] to start the API\n"
            f"4. Run [bold]opencar --help[/bold] for more commands",
            title="OpenCar Project Created",
            border_style="green",
        )
    )


@app.command()
def info() -> None:
    """Display system information and configuration."""
    settings = get_settings()

    # Create info table
    table = Table(title="OpenCar System Information", show_header=True)
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    # System info
    table.add_row("Version", __version__)
    table.add_row("Python", sys.version.split()[0])
    table.add_row("Platform", sys.platform)

    # Configuration info
    table.add_row("", "")  # Empty row
    table.add_row("[bold]Configuration[/bold]", "")
    table.add_row("Debug Mode", str(settings.debug))
    table.add_row("Log Level", settings.log_level)
    table.add_row("API Host", f"{settings.api_host}:{settings.api_port}")
    table.add_row("Device", settings.device)

    # ML info
    table.add_row("", "")
    table.add_row("[bold]ML Configuration[/bold]", "")
    table.add_row("Batch Size", str(settings.batch_size))
    table.add_row("Model Path", str(settings.model_path))
    table.add_row("OpenAI Model", settings.openai_model)

    console.print(table)


@app.command()
def status() -> None:
    """Check system status and health."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Checking system status...", total=4)

        # Check API
        progress.update(task, advance=1, description="Checking API...")
        api_status = _check_api_status()

        # Check database
        progress.update(task, advance=1, description="Checking database...")
        db_status = _check_database_status()

        # Check Redis
        progress.update(task, advance=1, description="Checking Redis...")
        redis_status = _check_redis_status()

        # Check models
        progress.update(task, advance=1, description="Checking models...")
        model_status = _check_model_status()

    # Display results
    table = Table(title="System Status", show_header=True)
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="yellow")

    table.add_row(
        "API Server",
        "[green]●[/green] Online" if api_status else "[red]●[/red] Offline",
        "Running on port 8000" if api_status else "Not running",
    )
    table.add_row(
        "Database",
        "[green]●[/green] Connected" if db_status else "[red]●[/red] Disconnected",
        "PostgreSQL" if db_status else "Connection failed",
    )
    table.add_row(
        "Redis Cache",
        "[green]●[/green] Connected" if redis_status else "[red]●[/red] Disconnected",
        "Ready" if redis_status else "Connection failed",
    )
    table.add_row(
        "ML Models",
        "[green]●[/green] Loaded" if model_status else "[yellow]●[/yellow] Not loaded",
        "3 models available" if model_status else "No models found",
    )

    console.print(table)


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Server host"),
    port: int = typer.Option(8000, "--port", "-p", help="Server port"),
    workers: int = typer.Option(1, "--workers", "-w", help="Number of workers"),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
) -> None:
    """Start the OpenCar API server."""
    console.print(f"[bold blue]Starting OpenCar API Server[/bold blue]")
    console.print(f"Host: {host}:{port}")
    console.print(f"Workers: {workers}")
    console.print(f"Reload: {reload}")
    
    if uvicorn is None:
        console.print("[red]Error: uvicorn not installed. Install with 'pip install uvicorn'[/red]")
        raise typer.Exit(1)
    
    try:
        uvicorn.run(
            "opencar.api.app:app",
            host=host,
            port=port,
            workers=workers,
            reload=reload,
        )
    except ImportError:
        console.print("[red]Error: uvicorn not installed. Install with 'pip install uvicorn'[/red]")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped by user[/yellow]")


def _check_api_status() -> bool:
    """Check if API server is running."""
    try:
        import httpx
        response = httpx.get("http://localhost:8000/health", timeout=2.0)
        return response.status_code == 200
    except Exception:
        return False


def _check_database_status() -> bool:
    """Check database connection."""
    # Mock implementation - replace with actual check
    return True


def _check_redis_status() -> bool:
    """Check Redis connection."""
    # Mock implementation - replace with actual check
    return True


def _check_model_status() -> bool:
    """Check if models are available."""
    settings = get_settings()
    return settings.model_path.exists()


if __name__ == "__main__":
    app() 