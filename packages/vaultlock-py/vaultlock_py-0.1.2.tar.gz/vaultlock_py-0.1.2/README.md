# vaultlock-py

[![PyPI version](https://badge.fury.io/py/vaultlock-py.svg)](https://badge.fury.io/py/vaultlock-py)
[![Downloads](https://pepy.tech/badge/vaultlock-py)](https://pepy.tech/project/vaultlock-py)

**vaultlock-py** is a secure Python library designed to unify and simplify secret management, cryptographic key handling, and secure operations across Google Cloud Secret Manager, Google Cloud KMS, and HashiCorp Vault.

Built with DevSecOps, cloud-native security, and modern cryptographic best practices in mind, this library allows Python developers and cloud engineers to lock down secrets, encrypt sensitive data, and securely integrate external key management systems into their apps or CI/CD pipelines.

## Features

vaultlock-py offers a powerful and unified key management interface that allows developers to manage, rotate, and retrieve secrets securely across platforms such as Google Cloud Secret Manager, HashiCorp Vault, and Google Cloud KMS. It supports end-to-end encryption using robust standards like AES-256, and enables envelope encryption with cloud-managed keys for enhanced security. The library includes a suite of command-line tools that make it easy to encrypt and decrypt files, manage secrets, and validate secure access from any environment. Designed with compliance and traceability in mind, vaultlock-py provides audit-friendly logging and access visibility, making it ideal for regulated environments. Its modular and extensible architecture ensures that users can selectively adopt components based on their infrastructure needs, whether they're working solely with Vault, KMS, or Secret Manager. Built with cloud-native principles, the library integrates seamlessly into modern CI/CD pipelines, Kubernetes clusters, and cloud-based applications.

## Use Cases

- Encrypting sensitive config files before storage.

- Centralized secret retrieval in production microservices.

- Secure data exchange across cloud environments.

- Building compliance-aware automation for regulated industries.

## Technologies Used

- Google Cloud Secret Manager

- HashiCorp Vault

- Google Cloud KMS

- HashiCorp Vault via hvac library

- Python 3.8+

- Follows PEP 621 and pyproject.toml standards

- Designed for use in CI/CD and container environments

## Installation
```bash
pip install vaultlock-py
```

## CLI Usage
```bash
python -m vaultlock.cli --mode gcp --action create --project_id=my-project --path=my-secret --value=secret123
```

## License

This README provides an overview, installation, usage examples (CLI and code), and a brief mention of how it works and license. In an actual project, one might expand the README with troubleshooting tips or more details on authentication.

MIT License

Copyright (c) 2025 Raghava Chellu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
