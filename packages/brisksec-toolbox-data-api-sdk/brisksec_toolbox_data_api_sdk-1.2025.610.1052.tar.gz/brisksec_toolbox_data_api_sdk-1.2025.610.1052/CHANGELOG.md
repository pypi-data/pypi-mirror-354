# Changelog

All notable changes to the Brisksec_toolbox_data_api_sdk will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-10

### Added
- Initial release of the Brisksec_toolbox_data_api_sdk
- Full async/await support with `.asyncio()` methods
- Synchronous support with `.sync()` methods
- Comprehensive type hints for better IDE support
- Automatic request/response serialization
- Built-in error handling and validation
- Coverage for all API endpoints

### Features
- POST /api/v1/organizations/
- GET /api/v1/organizations/
- GET /api/v1/organizations/{entity_id}
- PATCH /api/v1/organizations/{entity_id}
- DELETE /api/v1/organizations/{entity_id}
- GET /api/v1/organizations/{entity_id}/relationships
- POST /api/v1/domains/
- GET /api/v1/domains/
- GET /api/v1/domains/{entity_id}
- PATCH /api/v1/domains/{entity_id}
- DELETE /api/v1/domains/{entity_id}
- GET /api/v1/domains/{entity_id}/relationships
- GET /api/v1/domains/expiring/soon
- POST /api/v1/ip-addresses/
- GET /api/v1/ip-addresses/
- GET /api/v1/ip-addresses/{entity_id}
- PATCH /api/v1/ip-addresses/{entity_id}
- DELETE /api/v1/ip-addresses/{entity_id}
- GET /api/v1/ip-addresses/{entity_id}/relationships
- POST /api/v1/services/
- GET /api/v1/services/
- GET /api/v1/services/{entity_id}
- PATCH /api/v1/services/{entity_id}
- DELETE /api/v1/services/{entity_id}
- GET /api/v1/services/{entity_id}/relationships
- GET /api/v1/relationships/types
- GET /api/v1/relationships/types/{source_type}/{target_type}
- GET /api/v1/relationships/entity/{entity_type}/{entity_id}
- POST /api/v1/relationships/
- POST /api/v1/relationships/get
- PATCH /api/v1/relationships/update
- DELETE /api/v1/relationships/delete
- POST /api/v1/relationships/batch
- GET /
- GET /health


### Dependencies
- httpx >= 0.20.0
- attrs >= 22.2.0
- python-dateutil >= 2.8.0

---
*This SDK is auto-generated from the OpenAPI specification*