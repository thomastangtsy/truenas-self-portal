import os

config = {
    "api_key": os.environ.get("TRUENAS_API_KEY", ""),
    "endpoint": os.environ.get("TRUENAS_ENDPOINT", "https://127.0.0.1"),
    "ignore_invalid_certificate": os.environ.get("TRUENAS_IGNORE_CERTIFICATE", "0"),
}