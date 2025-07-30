# qlikreload

A small Python utility package to trigger Qlik Sense app reloads via the QRS API.

## Installation

```bash
pip install .
```

## Usage

```python
from qlikreload import QlikReloader

reloader = QlikReloader(
    server_url="https://qlikkls.swisscancer.ch",
    app_id="your-app-id",
    cert_path="client.pem",
    key_path="client_key.pem"
)

status, response = reloader.reload_app()
print("Status:", status)
print("Response:", response)
```
