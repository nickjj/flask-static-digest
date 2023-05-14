# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

- Nothing yet!

## [0.4.0] - 2023-05-14

- Brotli support added by [Dr. Matthew Swabey](https://github.com/mattaw)
- Remove `FLASK_STATIC_DIGEST_GZIP_FILES` gzip config option
- Add `FLASK_STATIC_DIGEST_COMPRESSION` (defaults to `["gzip"]` and replaces the old gzip config option)

## [0.3.0] - 2022-03-16

- Add support for digesting static files in blueprints and nested blueprints
- Spruce up the code base by using Black for code formatting

## [0.2.1] - 2020-12-23

### Fixed

- Ensure Flask's `static_url_path` is used if you have a host URL set

## [0.2.0] - 2020-12-23

### Added

- Support to prepend your static paths with a host / CDN URL via `FLASK_STATIC_DIGEST_HOST_URL`

## [0.1.4] - 2020-11-24

### Fixed

- `static_url_for` will now throw a 404 instead of a 500 if you have an invalid `filename`

## [0.1.3] - 2020-01-23

### Added

- Windows support

## [0.1.2] - 2019-10-30

### Fixed

- Really fix the version being read dynamically in `setup.py`

## [0.1.1] - 2019-10-30

### Fixed

- Attempt to fix the version being read dynamically in `setup.py`

## [0.1.0] - 2019-10-30

### Added

- Everything!

[Unreleased]: https://github.com/nickjj/flask-static-digest/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/nickjj/flask-static-digest/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/nickjj/flask-static-digest/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/nickjj/flask-static-digest/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/nickjj/flask-static-digest/compare/v0.1.4...v0.2.0
[0.1.4]: https://github.com/nickjj/flask-static-digest/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/nickjj/flask-static-digest/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/nickjj/flask-static-digest/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/nickjj/flask-static-digest/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/nickjj/flask-static-digest/releases/tag/v0.1.0
