# Brisksec toolbox data api sdk

> **Official Python SDK for the BriskSec Toolbox Data API**

[![PyPI version](https://badge.fury.io/py/brisksec_toolbox_data_api_sdk.svg)](https://badge.fury.io/py/brisksec_toolbox_data_api_sdk)
[![Python versions](https://img.shields.io/pypi/pyversions/brisksec_toolbox_data_api_sdk.svg)](https://pypi.org/project/brisksec_toolbox_data_api_sdk/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://github.com/brisksec/brisksec-toolbox-data-api-sdk/workflows/CI/badge.svg)](https://github.com/brisksec/brisksec-toolbox-data-api-sdk/actions)

Official Python SDK for the BriskSec Toolbox Data API

## 🚀 Quick Start

### Installation

```bash
pip install brisksec_toolbox_data_api_sdk
```

### Basic Usage

```python
import asyncio
from brisksec_toolbox_data_api_sdk.client import Client
from brisksec_toolbox_data_api_sdk.api.organizations import list_organizations

async def main():
    # Create client
    client = Client(base_url="")
    
    # List organizations
    response = await list_organizations.asyncio(
        client=client,
        page=1,
        size=10
    )
    
    print(f"Found {response.total} organizations")
    for org in response.items:
        print(f"- {org.name}: {org.description}")

# Run the example
asyncio.run(main())
```

## 📚 Documentation

### API Client

The SDK provides both synchronous and asynchronous clients:

```python
from brisksec_toolbox_data_api_sdk.client import Client, AuthenticatedClient

# Basic client
client = Client(base_url="")

# Authenticated client (if API requires authentication)
auth_client = AuthenticatedClient(
    base_url="",
    token="your-api-token"
)
```

### Available Endpoints

- **Organizations**: `brisksec_toolbox_data_api_sdk.api.organizations` - Organization management
- **Domains**: `brisksec_toolbox_data_api_sdk.api.domains` - Domain management  
- **IP Addresses**: `brisksec_toolbox_data_api_sdk.api.ip_addresses` - IP address management
- **Services**: `brisksec_toolbox_data_api_sdk.api.services` - Service management
- **Relationships**: `brisksec_toolbox_data_api_sdk.api.relationships` - Relationship management between assets

## 🔧 Usage Patterns

### Async Usage (Recommended)

```python
import asyncio
from brisksec_toolbox_data_api_sdk.client import Client
from brisksec_toolbox_data_api_sdk.api.organizations import create_organization, get_organization
from brisksec_toolbox_data_api_sdk.models.organization_create import OrganizationCreate

async def example_operations():
    client = Client(base_url="")
    
    # Create organization
    org_data = OrganizationCreate(
        name="Example Corp",
        description="Example organization"
    )
    
    new_org = await create_organization.asyncio(
        client=client,
        body=org_data
    )
    
    # Get organization
    org = await get_organization.asyncio(
        client=client,
        entity_id=new_org.id
    )
    
    return org

asyncio.run(example_operations())
```

### Sync Usage

```python
from brisksec_toolbox_data_api_sdk.client import Client
from brisksec_toolbox_data_api_sdk.api.organizations import list_organizations

def get_organizations():
    client = Client(base_url="")
    
    response = list_organizations.sync(
        client=client,
        page=1,
        size=50
    )
    
    return response.items

organizations = get_organizations()
```

### Error Handling

```python
import asyncio
from brisksec_toolbox_data_api_sdk.client import Client
from brisksec_toolbox_data_api_sdk.api.organizations import get_organization
from brisksec_toolbox_data_api_sdk import errors

async def safe_get_organization(org_id: str):
    client = Client(base_url="")
    
    try:
        response = await get_organization.asyncio(
            client=client,
            entity_id=org_id
        )
        return response
    except errors.UnexpectedStatus as e:
        print(f"API returned unexpected status: {e.status_code}")
        return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None
```

### Pagination

```python
async def get_all_organizations():
    client = Client(base_url="")
    all_orgs = []
    page = 1
    
    while True:
        response = await list_organizations.asyncio(
            client=client,
            page=page,
            size=100
        )
        
        all_orgs.extend(response.items)
        
        if len(response.items) < 100:  # Last page
            break
            
        page += 1
    
    return all_orgs
```

## ⚙️ Configuration

### Environment Variables

```bash
# API Base URL
export BRISKSEC_TOOLBOX_DATA_API_SDK_BASE_URL=""

# API Token (if authentication required)
export BRISKSEC_TOOLBOX_DATA_API_SDK_API_TOKEN="your-api-token"

# Request timeout (seconds)
export BRISKSEC_TOOLBOX_DATA_API_SDK_TIMEOUT="30"
```

### Client Configuration

```python
import httpx
from brisksec_toolbox_data_api_sdk.client import Client

# Custom timeout
client = Client(
    base_url="",
    timeout=httpx.Timeout(60.0)
)

# Custom headers
client = Client(base_url="")
client.headers.update({
    "X-Custom-Header": "value",
    "User-Agent": "MyApp/1.0"
})

# SSL verification (development only)
client = Client(
    base_url="",
    verify_ssl=False
)
```

## ✨ Features

- ✅ **Auto-generated** from OpenAPI specification
- ✅ **Full async/await support** with `.asyncio()` methods
- ✅ **Synchronous support** with `.sync()` methods  
- ✅ **Comprehensive type hints** for better IDE support
- ✅ **Automatic request/response serialization**
- ✅ **Built-in error handling and validation**
- ✅ **All API endpoints covered**
- ✅ **Pagination support**
- ✅ **Custom client configuration**

## 📦 Requirements

- Python 3.9+
- httpx >= 0.20.0
- attrs >= 22.2.0
- python-dateutil >= 2.8.0

## 📖 Examples

Check the `examples/` directory for complete usage examples:

- [`basic_usage.py`](examples/basic_usage.py) - Basic async/await usage
- [`sync_usage.py`](examples/sync_usage.py) - Synchronous usage patterns
- [`async_usage.py`](examples/async_usage.py) - Advanced async patterns

### Available Models

All request/response models are available in the `brisksec_toolbox_data_api_sdk.models` module:

```python
from brisksec_toolbox_data_api_sdk.models import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    DomainCreate,
    RelationshipCreate,
    # ... and more
)
```

## 🏗️ SDK Generation

This SDK is automatically generated from the BriskSec Toolbox Data API OpenAPI specification.

### Latest Generation

- **Generated**: {{ generation_timestamp or "Latest" }}
- **API Version**: {{ api_version or version }}
- **SDK Version**: 1.0.0

### Updates

The SDK is automatically updated when the API changes. Check the [releases page](https://github.com/brisksec/brisksec-toolbox-data-api-sdk/releases) for the latest version.

## 🤝 Contributing

This SDK is auto-generated. To suggest improvements:

1. **API Changes**: Submit issues to the [main API repository](https://github.com/brisksec/brisksec-toolbox-data-api-sdk)
2. **SDK Generation**: Contribute to the [SDK generation tools](https://github.com/brisksec/brisksec-toolbox-data-api-sdk/tree/main/tools/sdk)
3. **Documentation**: Help improve templates and examples

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This SDK is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🔗 Links

- **API Documentation**: [/docs](/docs)
- **OpenAPI Spec**: [/openapi.json](/openapi.json)
- **PyPI Package**: [https://pypi.org/project/brisksec_toolbox_data_api_sdk/](https://pypi.org/project/brisksec_toolbox_data_api_sdk/)
- **Source Repository**: [https://github.com/brisksec/brisksec-toolbox-data-api-sdk](https://github.com/brisksec/brisksec-toolbox-data-api-sdk)
- **Issue Tracker**: [https://github.com/brisksec/brisksec-toolbox-data-api-sdk/issues](https://github.com/brisksec/brisksec-toolbox-data-api-sdk/issues)
- **Documentation**: [https://brisksec.github.io/brisksec-toolbox-data-api-sdk](https://brisksec.github.io/brisksec-toolbox-data-api-sdk)

## 🆘 Support

- **API Documentation**: [/docs](/docs)
- **GitHub Issues**: [https://github.com/brisksec/brisksec-toolbox-data-api-sdk/issues](https://github.com/brisksec/brisksec-toolbox-data-api-sdk/issues)
- **Discussions**: [https://github.com/brisksec/brisksec-toolbox-data-api-sdk/discussions](https://github.com/brisksec/brisksec-toolbox-data-api-sdk/discussions)

---

**Generated with ❤️ by the BriskSec Toolbox Data API SDK Generator**

*Last updated: {{ generation_date or "Latest build" }}*