import typer
from rich.console import Console
from rich.table import Table
import qrcode

from . import storage, otp

app = typer.Typer()
console = Console()


@app.command()
def add(provider: str):
    """Add a new provider and its secret key."""
    key = typer.prompt(f"Enter the secret key for {provider}", hide_input=True)
    storage.set_key(provider, key)
    storage.add_provider_to_list(provider)
    console.print(f"[green]Provider '{provider}' added successfully.[/green]")


@app.command(name="list")
def list_providers():
    """List all configured providers."""
    providers = storage.get_all_providers()
    if not providers:
        console.print("[yellow]No providers configured yet.[/yellow]")
        return

    table = Table("Providers")
    for provider in providers:
        table.add_row(provider)
    console.print(table)


@app.command()
def remove(provider: str):
    """Remove a provider."""
    storage.remove_key(provider)
    storage.remove_provider_from_list(provider)
    console.print(f"[green]Provider '{provider}' removed successfully.[/green]")


@app.command()
def export(provider: str):
    """Export a provider's secret key as a QR code."""
    key = storage.get_key(provider)
    if not key:
        console.print(f"[red]Provider '{provider}' not found.[/red]")
        raise typer.Exit(code=1)

    uri = f"otpauth://totp/{provider}?secret={key}&issuer={provider}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)

    qr.make(fit=True)
    matrix = qr.get_matrix()

    console.print(f"Scan the QR code below to import the secret for '{provider}':")
    for row in matrix:
        line = ""
        for col in row:
            if col:
                line += "██"
            else:
                line += "  "
        console.print(line)


@app.command()
def get(provider: str):
    """Get the OTP for a provider."""
    key = storage.get_key(provider)
    if not key:
        console.print(f"[red]Provider '{provider}' not found.[/red]")
        raise typer.Exit(code=1)

    one_time_password, time_remaining = otp.get_otp(key)
    console.print(f"OTP for {provider}: [bold green]{one_time_password}[/bold green]")
    console.print(f"Time remaining: {time_remaining} seconds")


if __name__ == "__main__":
    app()
