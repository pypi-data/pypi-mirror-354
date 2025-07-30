import typer
from .calc.cli import app as calc_app

app = typer.Typer()
app.add_typer(calc_app, name="calc")
