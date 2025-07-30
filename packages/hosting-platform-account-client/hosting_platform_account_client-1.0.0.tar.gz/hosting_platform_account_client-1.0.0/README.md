# Account-service Client

**Proprietary Python client** for the account-service API.

## Installation

```bash
pip install hosting-platform-account-client
```

## Usage

```python
from account_service_client import ApiClient, Configuration
from account_service_client.api import DefaultApi

# Configure the client
configuration = Configuration(
    host="http://localhost:5001"  # Replace with your service URL
)

# Create API client
with ApiClient(configuration) as api_client:
    api_instance = DefaultApi(api_client)
    
    # Use the API...
    try:
        response = api_instance.health_get()
        print("Service is healthy:", response)
    except Exception as e:
        print("Error:", e)
```

## License

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

Version: 1.0.0
