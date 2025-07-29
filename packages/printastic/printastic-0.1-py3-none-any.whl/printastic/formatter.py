from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.json import JSON
from rich import box

console = Console()


def print_header(text: str):
    console.rule(f"[bold blue]{text}")


def print_success(message: str):
    console.print(f"[bold green]✔ {message}")


def print_warning(message: str):
    console.print(f"[bold yellow]⚠ {message}")


def print_error(message: str):
    console.print(f"[bold red]✖ {message}")


def print_dict(data: dict, title="Data", box_style=box.SIMPLE):
    table = Table(title=title, box=box_style)
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    for key, value in data.items():
        table.add_row(str(key), str(value))

    console.print(table)


def print_json(data: dict):
    console.print(JSON.from_data(data))


def print_panel(message: str, title="Info", style="bold white on black"):
    panel = Panel(message, title=title, style=style)
    console.print(panel)
