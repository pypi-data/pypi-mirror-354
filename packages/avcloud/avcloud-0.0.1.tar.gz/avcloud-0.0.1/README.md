# AVCloud SDK

A Python SDK for interfacing with AVCloud services.

## Overview

AVCloud SDK provides a simple and intuitive interface to interact with AVCloud services. This SDK is designed to be easy to use while providing robust functionality for developers building applications that integrate with AVCloud.

## Features

- **Simple API Client**: Easy-to-use client for AVCloud services
- **Type Safety**: Built with type hints for better development experience
- **Comprehensive Testing**: Full test suite with pytest
- **Modern Python**: Supports Python 3.13+


## Quick Start

```python
from avcloud.client import AvCloudClient

# Initialize the client
client = AvCloudClient(private_key_path="~/.ssh/avcloud_key.pem")

```

## Contributing

Interested in contributing? Please see our [Developer Guide](docs/dev/developer_guide.md) for detailed information on:


### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions and methods
- Write comprehensive tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes to this project. 