# akamai_papi

A Lightweight Python SDK for interacting with Akamai's Property Manager API (PAPI).

## Features
- Load credentials from `~/.edgerc`
- List groups and contracts
- Enumerate properties within groups
- Retrieve property rules for specific versions
- Pythonic interface to Akamai PAPI endpoints

## Installation
```bash
pip install akamai_papi
```

## Setup
Ensure your `~/.edgerc` file is correctly configured. Example:
```ini
[default]
client_token = your-client-token
client_secret = your-client-secret
access_token = your-access-token
host = your-host.luna.akamaiapis.net
```

## Usage
```python
from akamai_papi import PapiClient
client = PapiClient()
```

### List Groups
```python
groups = client.list_groups()
for group in groups:
    print(group['groupName'], group['groupId'])
```

### List Contracts
```python
contracts = client.list_contracts()
for contract in contracts:
    print(contract['contractId'], contract['contractType'])
```

### List Properties in a Group
```python
properties = client.list_properties(group_id=group['groupId'])
for prop in properties:
    print(prop['propertyName'], prop['propertyId'])
```

### Get Rules for a Property Version
```python
rules = client.get_property_rules(
    property_id=prop['propertyId'],
    version=prop['latestVersion'],
    group_id=group['groupId']
)
print(rules)
```

### Get All Versions of a Property
```python
versions = client.get_property_versions(prop['propertyId'], group['groupId'])
for version in versions:
    print(version['propertyVersion'], version['updatedDate'])
```

## Development
Clone the repo and install it in editable mode:
```bash
git clone https://github.com/yourusername/akamai_papi
cd akamai_papi
pip install -e .
```