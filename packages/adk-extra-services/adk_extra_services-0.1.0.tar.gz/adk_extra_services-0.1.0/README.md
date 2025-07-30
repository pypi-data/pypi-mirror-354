# ADK Extra Services

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python Tests](https://github.com/edu010101/adk-extra-services/actions/workflows/ci.yml/badge.svg)](https://github.com/edu010101/adk-extra-services/actions/workflows/ci.yml)

> Extensions and additional services for the [Agent Development Kit (ADK)](https://github.com/google/adk-python)

ADK Extra Services provides production-ready implementations of common services needed for building robust AI agents with the Google ADK framework.

## 🚀 Installation

```bash
pip install adk-extra-services
```

## 📖 Services

### 🔄 Sessions

Persistent session storage implementations for ADK agents.

#### Available Services:
- **MongoDBSessionService**: Persistent session storage using MongoDB
  ```python
  from adk_extra_services.sessions import MongoSessionService
  ```

- **RedisSessionService**: High-performance session storage using Redis
  ```python
  from adk_extra_services.sessions import RedisSessionService
  ```

For complete usage examples and API documentation, see the [Sessions Guide](examples/sessions/README.md).

### 📦 Artifacts

Storage and management of agent artifacts.

#### Available Services:
- **S3ArtifactService**: Store and manage artifacts in AWS S3 or compatible storage
  ```python
  from adk_extra_services.artifacts import S3ArtifactService
  ```

For complete usage examples and API documentation, see the [Artifacts Guide](examples/artifacts/README.md).

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

