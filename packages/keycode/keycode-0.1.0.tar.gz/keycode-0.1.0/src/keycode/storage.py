import keyring
import json


def set_key(provider: str, key: str):
    """Set the key for a specific provider."""
    keyring.set_password("keycode", provider, key)


def get_key(provider: str) -> str | None:
    """Get the key for a specific provider."""
    return keyring.get_password("keycode", provider)


def remove_key(provider: str):
    """Remove the key for a specific provider."""
    try:
        keyring.delete_password("keycode", provider)
    except keyring.errors.PasswordNotFoundError:
        pass


def get_all_providers() -> list[str]:
    """Get a list of all providers."""
    providers_json = keyring.get_password("keycode", "providers")
    if providers_json:
        return json.loads(providers_json)
    return []


def add_provider_to_list(provider: str):
    """Add a provider to the list of providers."""
    providers = get_all_providers()
    if provider not in providers:
        providers.append(provider)
        keyring.set_password("keycode", "providers", json.dumps(providers))


def remove_provider_from_list(provider: str):
    """Remove a provider from the list of providers."""
    providers = get_all_providers()
    if provider in providers:
        providers.remove(provider)
        keyring.set_password("keycode", "providers", json.dumps(providers))
