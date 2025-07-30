"""Command line interface for Skytup."""
import click
from . import hello, add

@click.group()
def cli():
    """Skytup CLI - A sample Python package CLI."""
    pass

@cli.command()
def greet():
    """Print a friendly greeting."""
    click.echo(hello())

@cli.command()
@click.argument('a', type=float)
@click.argument('b', type=float)
def sum(a, b):
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    """
    result = add(a, b)
    click.echo(f"The sum of {a} and {b} is {result}")

if __name__ == '__main__':
    cli()
