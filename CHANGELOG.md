# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- `MyTextError` class
- `MyTextValidationError` class
- `MyTextProviderError` class
### Changed
- `grammar` mode optimized
- Instructions modified
## [0.7] - 2026-04-24
### Added
- `emojify` mode
- `biblical` tone
- `viking` tone
- `zen` tone
- `corporate` tone
- Tone hint
### Changed
- `README.md` updated
- Cerebras default model changed to `llama3.1-8b`
- Instructions modified
## [0.6] - 2026-03-11
### Added
- GitHub provider
### Changed
- CLI functions moved to `cli.py`
- CLI messages updated
- CLI modified
- OpenRouter default model changed to `openai/gpt-oss-20b:free`
- Test system modified
- `README.md` updated
## [0.5] - 2026-02-18
### Added
- `--provider` argument
- `--model` argument
- `_load_model_from_env` function
### Changed
- `model` parameter added to `run_mytext` function
- AI Studio default model changed to `gemma-3-1b-it`
- OpenRouter default model changed to `google/gemma-3-27b-it:free`
- Test system modified
- `README.md` updated
## [0.4] - 2025-12-25
### Added
- Groq provider
- NVIDIA provider
- `--loop` argument
### Changed
- Test system modified
- `README.md` updated
## [0.3] - 2025-12-17
### Added
- OpenRouter provider
- Cerebras provider
### Changed
- Test system modified
- `README.md` updated
- AI Studio main model changed to `gemini-2.5-flash`
- AI Studio fallback model changed to `gemma-3-1b-it`
- Providers moved to `providers.py`
## [0.2] - 2025-12-05
### Added
- Logo
- `summarize` mode
- `simplify` mode
- `bulletize` mode
- `shorten` mode
### Changed
- `README.md` updated
- Cloudflare fallback model changed to `meta/llama-3.1-8b-instruct-fast`
- Model switching modified
## [0.1] - 2025-11-26
### Added
- `run_mytext` function
- AI Studio provider
- Cloudflare provider
- `--mode` argument
- `--tone` argument

[Unreleased]: https://github.com/sepandhaghighi/mytext/compare/v0.7...dev
[0.7]: https://github.com/sepandhaghighi/mytext/compare/v0.6...v0.7
[0.6]: https://github.com/sepandhaghighi/mytext/compare/v0.5...v0.6
[0.5]: https://github.com/sepandhaghighi/mytext/compare/v0.4...v0.5
[0.4]: https://github.com/sepandhaghighi/mytext/compare/v0.3...v0.4
[0.3]: https://github.com/sepandhaghighi/mytext/compare/v0.2...v0.3
[0.2]: https://github.com/sepandhaghighi/mytext/compare/v0.1...v0.2
[0.1]: https://github.com/sepandhaghighi/mytext/compare/dde63ee...v0.1



