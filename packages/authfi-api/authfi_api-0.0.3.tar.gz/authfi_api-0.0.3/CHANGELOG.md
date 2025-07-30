# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-11

### Added
- Initial release of AuthFi API Python wrapper
- Complete WebAuthn/FIDO2 registration and authentication support
- Mobile authenticator app support with QR code generation
- User management functionality (list, create, suspend, delete)
- Credential management (list, rename, delete keys)
- Comprehensive error handling with descriptive messages
- Type hints and validation using Pydantic
- Full API coverage for Authentrend AuthFi service

### Features
- WebAuthn registration and login flows
- Mobile/non-passkey authentication flows
- QR code generation for mobile registration and verification
- User state management (activate/suspend)
- Credential management and naming
- Pagination support for user listing
- Configurable timeout and authentication parameters
- Comprehensive test suite