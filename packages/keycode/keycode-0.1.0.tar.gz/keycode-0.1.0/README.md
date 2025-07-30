# keycode

A command-line tool for managing Time-based One-Time Passwords (TOTP).

## Installation

To install `keycode`, you can use `pip` or `uv`:

```bash
# Using pip
pip install .

# Using uv
uv pip install .
```

## Usage

`keycode` provides a simple interface for managing your TOTP secrets.

### Add a new provider

To add a new provider, use the `add` command:

```bash
keycode add <provider-name>
```

You will be prompted to enter the secret key for the provider.

### List all providers

To see a list of all your configured providers, use the `list` command:

```bash
keycode list
```

### Get an OTP

To get the current OTP for a specific provider, use the `get` command:

```bash
keycode get <provider-name>
```

### Remove a provider

To remove a provider and its associated secret key, use the `remove` command:

```bash
keycode remove <provider-name>
```

### Export a provider

To export a provider's secret key as a QR code, use the `export` command:

```bash
keycode export <provider-name>
```

This will display a QR code in your terminal that you can scan with an authenticator app to import the secret key.

