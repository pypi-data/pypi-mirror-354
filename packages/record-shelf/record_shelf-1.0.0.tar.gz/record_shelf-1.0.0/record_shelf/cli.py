#!/usr/bin/env python3
"""
Record Shelf

A tool for creating custom reports from music collection data
with sorting by shelf and then alphabetically.
"""

from pathlib import Path
from typing import Any, Dict, List

import click
import discogs_client
import pandas as pd
from tqdm import tqdm

from .config import Config
from .report_generator import ReportGenerator
from .utils import setup_logging


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
def cli(ctx, debug):
    """Record Shelf - Music Collection Reports Tool"""
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    setup_logging(debug)


@cli.command()
@click.option("--token", help="Discogs API token (or set DISCOGS_TOKEN env var)")
@click.option("--username", required=True, help="Discogs username")
@click.option(
    "--output", "-o", default="collection_report.xlsx", help="Output file path"
)
@click.option("--shelf", help="Filter by specific shelf (optional)")
@click.option(
    "--format",
    type=click.Choice(["xlsx", "csv", "html"]),
    default="xlsx",
    help="Output format",
)
@click.pass_context
def generate(ctx, token, username, output, shelf, format):
    """Generate a custom Discogs collection report"""
    try:
        config = Config(token=token, debug=ctx.obj["debug"])
        generator = ReportGenerator(config)

        click.echo(f"Fetching collection for user: {username}")
        report_data = generator.fetch_collection_data(username, shelf_filter=shelf)

        click.echo(f"Generating report with {len(report_data)} items...")
        generator.create_report(report_data, output, format)

        click.echo(f"Report saved to: {output}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--token", help="Discogs API token (or set DISCOGS_TOKEN env var)")
@click.option("--username", required=True, help="Discogs username")
def list_shelves(token, username):
    """List all shelves in the user's collection"""
    try:
        config = Config(token=token)
        generator = ReportGenerator(config)

        shelves = generator.get_user_shelves(username)

        click.echo("Available shelves:")
        for shelf in shelves:
            click.echo(f"  - {shelf}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


def main() -> None:
    """Main entry point for the CLI application."""
    cli()


if __name__ == "__main__":
    main()
